import time
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

SERVO_GPIO = 22

# Typical hobby servo range. Tighten these if the servo buzzes/slams.
MIN_PW_S = 0.5 / 1000   # 0.5 ms
MAX_PW_S = 2.5 / 1000   # 2.5 ms

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def angle_to_value(angle_deg: float) -> float:
    """
    Map 0..180 degrees to gpiozero Servo.value range (-1..+1).
    """
    angle_deg = clamp(angle_deg, 0.0, 180.0)
    return (angle_deg / 90.0) - 1.0  # 0->-1, 90->0, 180->+1

def main():
    factory = PiGPIOFactory()  # uses pigpiod (hardware-timed pulses)
    servo = Servo(
        SERVO_GPIO,
        pin_factory=factory,
        min_pulse_width=MIN_PW_S,
        max_pulse_width=MAX_PW_S,
    )

    try:
        # Center
        servo.value = angle_to_value(90)
        time.sleep(1.5)

        # Sweep 0 -> 180 -> 0
        for a in range(0, 181, 5):
            servo.value = angle_to_value(a)
            time.sleep(0.03)

        for a in range(180, -1, -5):
            servo.value = angle_to_value(a)
            time.sleep(0.03)

        # Back to center
        servo.value = angle_to_value(90)
        time.sleep(1.0)

    finally:
        servo.detach()

if __name__ == "__main__":
    main()

