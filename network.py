import asyncio
from dataclasses import dataclass
from typing import Sequence, Optional
from cmd import run_cmd

# Commands to manage connection:
# nmcli dev wifi connect orb_IoT
# nmcli connection up Ostara-Cam-AP

SUDO_PATH = "/usr/bin/sudo"
NMCLI_PATH = "/usr/bin/nmcli"


async def is_ap_mode():
    rc, out, err = await run_cmd(NMCLI_PATH, "-t", "-f", "NAME,DEVICE", "connection", "show", "--active", check=False, timeout=5)

    return any(line.startswith("Ostara-Cam") for line in out.splitlines())

# Assumptions:
# - AP connection "Ostara-Cam-AP" uses ipv4.method shared (NM handles DHCP/NAT)
# - /etc/dnsmasq.d/captive.conf binds to wlan0, uses port=5353, and address=/#/10.42.0.1
# - Your portal HTTP server listens on port 80 on the Pi

CAPTIVE_DNS_PID = "/run/captive-dnsmasq.pid"

async def start_captive_portal():
    # Stop ONLY our captive dnsmasq if it exists (do NOT pkill dnsmasq)
    await run_cmd(
        SUDO_PATH, "sh", "-c",
        f"test -f {CAPTIVE_DNS_PID} && kill $(cat {CAPTIVE_DNS_PID}) || true",
        check=False,
    )

    # Disconnect wlan0 from any client network, then bring up the AP
    await run_cmd(SUDO_PATH, "-n", NMCLI_PATH, "device", "disconnect", "wlan0", check=False)
    await run_cmd(SUDO_PATH, "-n", NMCLI_PATH, "-w", "30", "connection", "up", "Ostara-Cam-AP", check=True)

    # Start captive DNS (5353) with a PID file so we can stop it safely later
    await run_cmd(
        SUDO_PATH,
        "dnsmasq",
        "--conf-file=/etc/dnsmasq.d/captive.conf",
        f"--pid-file={CAPTIVE_DNS_PID}",
        check=True,
    )

    # Reset nft captive table
    await run_cmd(SUDO_PATH, "nft", "delete", "table", "ip", "captive", check=False)
    await run_cmd(SUDO_PATH, "nft", "add", "table", "ip", "captive", check=True)

    # NAT prerouting hook for redirects
    await run_cmd(
        SUDO_PATH, "nft", "add", "chain", "ip", "captive", "prerouting",
        "{", "type", "nat", "hook", "prerouting", "priority", "-100;", "}",
        check=True,
    )

    # Pure captive: drop forwarding (no internet)
    await run_cmd(
        SUDO_PATH, "nft", "add", "chain", "ip", "captive", "forward",
        "{", "type", "filter", "hook", "forward", "priority", "0;", "policy", "drop;", "}",
        check=True,
    )

    # DNS hijack: redirect client DNS (53) -> our dnsmasq (5353)
    await run_cmd(
        SUDO_PATH, "nft", "add", "rule", "ip", "captive", "prerouting",
        "iif", "wlan0", "udp", "dport", "53", "redirect", "to", ":5353",
        check=True,
    )
    await run_cmd(
        SUDO_PATH, "nft", "add", "rule", "ip", "captive", "prerouting",
        "iif", "wlan0", "tcp", "dport", "53", "redirect", "to", ":5353",
        check=True,
    )

    # HTTP captive: redirect all HTTP to local portal (80)
    await run_cmd(
        SUDO_PATH, "nft", "add", "rule", "ip", "captive", "prerouting",
        "iif", "wlan0", "tcp", "dport", "80", "redirect", "to", ":80",
        check=True,
    )


async def clear_captive_portal():
    # Stop ONLY our captive dnsmasq
    await run_cmd(
        SUDO_PATH, "sh", "-c",
        f"test -f {CAPTIVE_DNS_PID} && kill $(cat {CAPTIVE_DNS_PID}) || true; rm -f {CAPTIVE_DNS_PID}",
        check=False,
    )

    # Remove nft rules
    await run_cmd(SUDO_PATH, "nft", "delete", "table", "ip", "captive", check=False)

    # Bring down the AP
    await run_cmd(SUDO_PATH, "-n", NMCLI_PATH, "connection", "down", "Ostara-Cam-AP", check=False)

    # Optional: allow Wi-Fi to reconnect to normal networks
    await run_cmd(SUDO_PATH, "-n", NMCLI_PATH, "radio", "wifi", "on", check=False)

AP_CON = "Ostara-Cam-AP"
IFACE = "wlan0"

async def connect_ssid(ssid: str, password: str):
    # 0) Make sure wlan0 is not in AP mode / not bound to the AP connection
    #await run_cmd(SUDO_PATH, "-n", NMCLI_PATH, "connection", "down", AP_CON, check=False)
    #await run_cmd(SUDO_PATH, "-n", NMCLI_PATH, "device", "disconnect", IFACE, check=False)

    #Delete potential collision or existing connection 
    await run_cmd(SUDO_PATH, "-n", NMCLI_PATH, "connection", "delete", ssid, check=False) 

    # Force a scan to get updated SSIDs 
    await run_cmd(SUDO_PATH, "-n", NMCLI_PATH, "device", "wifi", "rescan", "ifname", "wlan0", check=False) 

    await asyncio.sleep(2)

    # Connect using known profile 
    await run_cmd(SUDO_PATH, "-n", NMCLI_PATH, "device", "wifi", "connect", ssid, "password", password, "ifname", "wlan0")

    # 1) Rescan so NM has fresh AP list
    #await run_cmd(SUDO_PATH, "-n", NMCLI_PATH, "device", "wifi", "rescan", "ifname", IFACE, check=False)
    #await asyncio.sleep(2)

    ## 2) Connect (this creates/updates a profile automatically)
    #rc, out, err = await run_cmd(
    #    SUDO_PATH, "-n",
    #    NMCLI_PATH, "-w", "30",
    #    "device", "wifi", "connect", ssid,
    #    "password", password,
    #    "ifname", IFACE,
    #    check=False,
    #)

    #print("rc=", rc)
    #print("err=", err)
    #print("out=", out)

    #if rc != 0:
    #    raise RuntimeError(f"nmcli wifi connect failed rc={rc}\nstdout:\n{out}\nstderr:\n{err}")

    ## 3) Verify we actually associated to the SSID
    #_, dev_out, _ = await run_cmd(
    #    NMCLI_PATH, "-t",
    #    "-f", "GENERAL.STATE,GENERAL.CONNECTION,IP4.ADDRESS",
    #    "device", "show", IFACE,
    #    check=True,
    #)
    #if ssid not in dev_out:
    #    raise RuntimeError(f"Connect did not stick.\n{dev_out}")

    #return out

