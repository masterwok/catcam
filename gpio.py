import asyncio
from gpiozero import Button, LED
from network import is_ap_mode, start_captive_portal
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",

)

logger = logging.getLogger(__name__)


BUTTON_GPIO = 4
LED_GPIO = 27

def init_gpio(app, loop: asyncio.AbstractEventLoop) -> None:
    button = Button(BUTTON_GPIO, pull_up=False, hold_time=1.0)
    led = LED(LED_GPIO)

    async def on_held():
        if not await is_ap_mode():
            print("Entering AP mode...")
            led.blink(on_time=0.5, off_time=0.5, background=True)
            await start_captive_portal()

    def on_held_async_delegate():
        fut = asyncio.run_coroutine_threadsafe(on_held(), loop)
        def _done(f):
            exc = f.exception()
            if exc:
                print(f"[gpio] on_held failed: {exc!r}")
        fut.add_done_callback(_done)

    button.when_held = on_held_async_delegate

    # Persist references
    app.state.gpio_button = button
    app.state.gpio_led = led

# -------- LED control helpers --------

def led_on(app):
    app.state.gpio_led.on()

def led_off(app):
    app.state.gpio_led.off()

def led_blink(app, on=0.5, off=0.5):
    app.state.gpio_led.blink(on_time=on, off_time=off, background=True)

def led_stop(app):
    app.state.gpio_led.off()
