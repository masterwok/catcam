import time
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

SERVO_GPIO = 22

MIN_PW_S = 0.5 / 1000
MAX_PW_S = 2.5 / 1000

def run_for_seconds(
    servo: Servo,
    seconds: float,
    speed: float = 0.6,
    direction: int = 1,
    settle_s: float = 0.05,
) -> None:
    if direction not in (1, -1):
        raise ValueError("direction must be +1 or -1")

    speed = max(0.0, min(1.0, speed))
    servo.value = direction * speed
    time.sleep(seconds)
    servo.value = 0.0
    time.sleep(settle_s)

def main():
    factory = PiGPIOFactory()
    servo = Servo(
        SERVO_GPIO,
        pin_factory=factory,
        min_pulse_width=MIN_PW_S,
        max_pulse_width=MAX_PW_S,
    )

    try:
        # Run CW for 1.25 seconds
        run_for_seconds(servo, seconds=2, speed=0.5, direction=1)

        time.sleep(1.0)

        # Run CCW for 0.75 seconds
        run_for_seconds(servo, seconds=2, speed=0.5, direction=-1)

    finally:
        servo.detach()

if __name__ == "__main__":
    main()

