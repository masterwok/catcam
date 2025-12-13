import asyncio
from dataclasses import dataclass
from typing import Sequence, Optional
from cmd import run_cmd

# Commands to manage connection:
# nmcli dev wifi connect orb_IoT
# nmcli connection up Ostara-Cam-AP

async def is_ap_mode():
    rc, out, err = await run_cmd("nmcli", "-t", "-f", "NAME,DEVICE", "connection", "show", "--active", check=False, timeout=5)

    return any(line.startswith("Ostara-Cam") for line in out.splitlines())

# Assumptions:
# - AP connection "Ostara-Cam-AP" uses ipv4.method shared (NM handles DHCP/NAT)
# - /etc/dnsmasq.d/captive.conf binds to wlan0, uses port=5353, and address=/#/10.42.0.1
# - Your portal HTTP server listens on port 80 on the Pi

CAPTIVE_DNS_PID = "/run/captive-dnsmasq.pid"

async def start_captive_portal():
    # Stop ONLY our captive dnsmasq if it exists (do NOT pkill dnsmasq)
    await run_cmd(
        "sudo", "sh", "-c",
        f"test -f {CAPTIVE_DNS_PID} && kill $(cat {CAPTIVE_DNS_PID}) || true",
        check=False,
    )

    # Disconnect wlan0 from any client network, then bring up the AP
    await run_cmd("sudo", "-n", "nmcli", "device", "disconnect", "wlan0", check=False)
    await run_cmd("sudo", "-n", "nmcli", "-w", "30", "connection", "up", "Ostara-Cam-AP", check=True)

    # Start captive DNS (5353) with a PID file so we can stop it safely later
    await run_cmd(
        "sudo",
        "dnsmasq",
        "--conf-file=/etc/dnsmasq.d/captive.conf",
        f"--pid-file={CAPTIVE_DNS_PID}",
        check=True,
    )

    # Reset nft captive table
    await run_cmd("sudo", "nft", "delete", "table", "ip", "captive", check=False)
    await run_cmd("sudo", "nft", "add", "table", "ip", "captive", check=True)

    # NAT prerouting hook for redirects
    await run_cmd(
        "sudo", "nft", "add", "chain", "ip", "captive", "prerouting",
        "{", "type", "nat", "hook", "prerouting", "priority", "-100;", "}",
        check=True,
    )

    # Pure captive: drop forwarding (no internet)
    await run_cmd(
        "sudo", "nft", "add", "chain", "ip", "captive", "forward",
        "{", "type", "filter", "hook", "forward", "priority", "0;", "policy", "drop;", "}",
        check=True,
    )

    # DNS hijack: redirect client DNS (53) -> our dnsmasq (5353)
    await run_cmd(
        "sudo", "nft", "add", "rule", "ip", "captive", "prerouting",
        "iif", "wlan0", "udp", "dport", "53", "redirect", "to", ":5353",
        check=True,
    )
    await run_cmd(
        "sudo", "nft", "add", "rule", "ip", "captive", "prerouting",
        "iif", "wlan0", "tcp", "dport", "53", "redirect", "to", ":5353",
        check=True,
    )

    # HTTP captive: redirect all HTTP to local portal (80)
    await run_cmd(
        "sudo", "nft", "add", "rule", "ip", "captive", "prerouting",
        "iif", "wlan0", "tcp", "dport", "80", "redirect", "to", ":80",
        check=True,
    )


async def clear_captive_portal():
    # Stop ONLY our captive dnsmasq
    await run_cmd(
        "sudo", "sh", "-c",
        f"test -f {CAPTIVE_DNS_PID} && kill $(cat {CAPTIVE_DNS_PID}) || true; rm -f {CAPTIVE_DNS_PID}",
        check=False,
    )

    # Remove nft rules
    await run_cmd("sudo", "nft", "delete", "table", "ip", "captive", check=False)

    # Bring down the AP
    await run_cmd("sudo", "-n", "nmcli", "connection", "down", "Ostara-Cam-AP", check=False)

    # Optional: allow Wi-Fi to reconnect to normal networks
    await run_cmd("sudo", "-n", "nmcli", "radio", "wifi", "on", check=False)

