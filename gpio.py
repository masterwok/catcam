import asyncio
import time
import logging

from gpiozero import Button, LED, Servo
from gpiozero.pins.pigpio import PiGPIOFactory

from network import is_ap_mode, start_captive_portal

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

BUTTON_GPIO = 4
LED_GPIO = 27

# Servo (continuous rotation / "360°")
SERVO_GPIO = 22
MIN_PW_S = 0.5 / 1000   # 0.5 ms
MAX_PW_S = 2.5 / 1000   # 2.5 ms


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def init_gpio(app, loop: asyncio.AbstractEventLoop) -> None:
    button = Button(BUTTON_GPIO, pull_up=False, hold_time=1.0)
    led = LED(LED_GPIO)

    # Servo: use pigpio for stable pulses
    factory = PiGPIOFactory()
    servo = Servo(
        SERVO_GPIO,
        pin_factory=factory,
        min_pulse_width=MIN_PW_S,
        max_pulse_width=MAX_PW_S,
    )
    servo.value = 0.0  # stop at startup

    # Prevent concurrent servo runs (two requests at once)
    servo_lock = asyncio.Lock()

    async def on_held():
        logger.info("Entering AP mode...")
        led.blink(on_time=0.5, off_time=0.5, background=True)
        await start_captive_portal()

    def on_held_async_delegate():
        fut = asyncio.run_coroutine_threadsafe(on_held(), loop)

        def _done(f):
            exc = f.exception()
            if exc:
                logger.exception("[gpio] on_held failed", exc_info=exc)

        fut.add_done_callback(_done)

    button.when_held = on_held_async_delegate

    # Persist references
    app.state.gpio_button = button
    app.state.gpio_led = led

    # Servo state on app
    app.state.gpio_servo = servo
    app.state.gpio_servo_lock = servo_lock


# -------- LED control helpers --------

def led_on(app):
    app.state.gpio_led.on()

def led_off(app):
    app.state.gpio_led.off()

def led_blink(app, on=0.5, off=0.5):
    app.state.gpio_led.blink(on_time=on, off_time=off, background=True)

def led_stop(app):
    app.state.gpio_led.off()


# -------- Servo control helpers --------

def _servo_run_for_seconds_blocking(
    servo: Servo,
    seconds: float,
    *,
    speed: float,
    direction: int,
    settle_s: float,
) -> None:
    if direction not in (1, -1):
        raise ValueError("direction must be +1 or -1")
    if seconds < 0:
        raise ValueError("seconds must be >= 0")

    speed = _clamp(speed, 0.0, 1.0)

    servo.value = direction * speed
    time.sleep(seconds)
    servo.value = 0.0
    time.sleep(settle_s)

async def servo_run_for_seconds(
    app,
    seconds: float,
    *,
    speed: float = 0.6,
    direction: int = 1,
    settle_s: float = 0.05,
) -> None:
    """
    Async-safe entrypoint for FastAPI handlers.
    Runs the blocking sleep in a worker thread and serializes access with a lock.
    """
    async with app.state.gpio_servo_lock:
        await asyncio.to_thread(
            _servo_run_for_seconds_blocking,
            app.state.gpio_servo,
            seconds,
            speed=speed,
            direction=direction,
            settle_s=settle_s,
        )
