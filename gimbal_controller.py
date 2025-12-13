import time
import smbus
import logging

# ==================== PCA9685 CONSTANTS ====================

PCA9685_MODE1    = 0x00
PCA9685_PRESCALE = 0xFE
LED0_ON_L        = 0x06

# Adjust these to your wiring / design
SERVO_UP_CH      = 0     # PCA9685 channel for "up/down" servo (pitch)
SERVO_DOWN_CH    = 1     # PCA9685 channel for "left/right" servo (yaw)

SERVO_UP_MIN     = 0
SERVO_UP_MAX     = 180
SERVO_DOWN_MIN   = 0
SERVO_DOWN_MAX   = 180

DEFAULT_STEP       = 5     # degrees per move command
DEFAULT_STEP_DELAY = 50    # ms between movements

logger = logging.getLogger(__name__)

class GimbalController:
    """
    PCA9685-based two-servo gimbal controller.

    - Uses SERVO_UP_CH for up/down (pitch)
    - Uses SERVO_DOWN_CH for left/right (yaw)

    Typical usage:

        gimbal = GimbalController()
        gimbal.move_up()
        gimbal.move_right(step=10)
    """

    def __init__(
        self,
        i2c_bus: int = 1,
        address: int = 0x40,
        freq_hz: float = 60.0,
        up_channel: int = SERVO_UP_CH,
        down_channel: int = SERVO_DOWN_CH,
        step_deg: int = DEFAULT_STEP,
        step_delay_ms: int = DEFAULT_STEP_DELAY,
    ) -> None:
        self.address = address
        self.up_channel = up_channel
        self.down_channel = down_channel
        self.step_deg = step_deg
        self.step_delay_ms = step_delay_ms

        # servo state
        self.servo_up_degree = 90
        self.servo_down_degree = 90

        # init I2C
        self.bus = smbus.SMBus(i2c_bus)

        # configure PCA9685
        self._set_pwm_freq(freq_hz)

        # initialize both servos to 90°
        self.set_servo_degree(self.up_channel, self.servo_up_degree)
        self.set_servo_degree(self.down_channel, self.servo_down_degree)

    # ==================== LOW-LEVEL I2C ====================

    def _read_reg(self, reg_addr: int) -> int:
        return self.bus.read_byte_data(self.address, reg_addr)

    def _write_reg(self, reg_addr: int, data: int) -> None:
        self.bus.write_byte_data(self.address, reg_addr & 0xFF, data & 0xFF)

    # ==================== PCA9685 CONTROL ====================

    def _set_pwm_freq(self, freq: float) -> None:
        """Set PCA9685 PWM frequency (Hz)."""
        freq *= 0.8449  # match your original C correction

        prescaleval = 25000000.0  # 25MHz
        prescaleval /= 4096.0     # 4096 steps
        prescaleval /= freq
        prescaleval -= 1.0
        prescale = int(prescaleval + 0.5)

        oldmode = self._read_reg(PCA9685_MODE1)
        newmode = (oldmode & 0x7F) | 0x10  # sleep

        self._write_reg(PCA9685_MODE1, newmode)      # go to sleep
        self._write_reg(PCA9685_PRESCALE, prescale)  # set prescaler
        self._write_reg(PCA9685_MODE1, oldmode)      # wake up
        time.sleep(0.005)
        self._write_reg(PCA9685_MODE1, oldmode | 0xA0)  # auto-increment on

    def _set_pwm(self, channel: int, on: int, off: int) -> None:
        base = LED0_ON_L + 4 * channel
        self._write_reg(base + 0, on & 0xFF)
        self._write_reg(base + 1, (on >> 8) & 0xFF)
        self._write_reg(base + 2, off & 0xFF)
        self._write_reg(base + 3, (off >> 8) & 0xFF)

    # ==================== SERVO HELPERS ====================

    def _set_servo_pulse(self, channel: int, pulse_seconds: float) -> None:
        """
        Set servo pulse width in seconds (matches your C mapping).
        """
        pulselength = 1000.0     # 1000 ms per second
        pulselength /= 60.0      # 60 Hz
        pulselength /= 4096.0

        ms = pulse_seconds * 1000.0
        ticks = int(ms / pulselength)

        self._set_pwm(channel, 0, ticks)

    def set_servo_degree(self, channel: int, degree: int) -> None:
        """
        Set servo angle in degrees [0, 180], using:
        pulse = (Degree + 45) / (90.0 * 1000);
        """
        if degree >= 180:
            degree = 180
        elif degree <= 0:
            degree = 0

        pulse = (degree + 45) / (90.0 * 1000.0)
        self._set_servo_pulse(channel, pulse)

    # ==================== INTERNAL DEGREE UP/DOWN ====================

    def _increase_degree(self, channel: int, step: int) -> None:
        if channel == self.up_channel:
            if self.servo_up_degree >= SERVO_UP_MAX:
                self.servo_up_degree = SERVO_UP_MAX
            else:
                self.servo_up_degree += step
                if self.servo_up_degree > SERVO_UP_MAX:
                    self.servo_up_degree = SERVO_UP_MAX
            self.set_servo_degree(channel, self.servo_up_degree)

        elif channel == self.down_channel:
            if self.servo_down_degree >= SERVO_DOWN_MAX:
                self.servo_down_degree = SERVO_DOWN_MAX
            else:
                self.servo_down_degree += step
                if self.servo_down_degree > SERVO_DOWN_MAX:
                    self.servo_down_degree = SERVO_DOWN_MAX
            self.set_servo_degree(channel, self.servo_down_degree)

        time.sleep(self.step_delay_ms / 1000.0)

    def _decrease_degree(self, channel: int, step: int) -> None:
        if channel == self.up_channel:
            if self.servo_up_degree <= SERVO_UP_MIN + step:
                self.servo_up_degree = SERVO_UP_MIN
            else:
                self.servo_up_degree -= step
                if self.servo_up_degree < SERVO_UP_MIN:
                    self.servo_up_degree = SERVO_UP_MIN
            self.set_servo_degree(channel, self.servo_up_degree)

        elif channel == self.down_channel:
            if self.servo_down_degree <= SERVO_DOWN_MIN + step:
                self.servo_down_degree = SERVO_DOWN_MIN
            else:
                self.servo_down_degree -= step
                if self.servo_down_degree < SERVO_DOWN_MIN:
                    self.servo_down_degree = SERVO_DOWN_MIN
            self.set_servo_degree(channel, self.servo_down_degree)

        time.sleep(self.step_delay_ms / 1000.0)

    # ==================== PUBLIC DIRECTION METHODS ====================

    def move_up(self, step: int | None = None) -> None:
        logger.info("UP")
        """Tilt up (decrease pitch angle or however you've oriented it)."""
        s = step if step is not None else self.step_deg
        self._increase_degree(self.up_channel, s)

    def move_down(self, step: int | None = None) -> None:
        logger.info("DOWN")
        """Tilt down."""
        s = step if step is not None else self.step_deg
        self._decrease_degree(self.up_channel, s)

    def move_right(self, step: int | None = None) -> None:
        """Pan right."""
        s = step if step is not None else self.step_deg
        self._increase_degree(self.down_channel, s)

    def move_left(self, step: int | None = None) -> None:
        """Pan left."""
        s = step if step is not None else self.step_deg
        self._decrease_degree(self.down_channel, s)

    def center(self) -> None:
        """Center both servos at 90°."""
        self.servo_up_degree = 90
        self.servo_down_degree = 90
        self.set_servo_degree(self.up_channel, self.servo_up_degree)
        self.set_servo_degree(self.down_channel, self.servo_down_degree)

    def close(self) -> None:
        """Close the I2C bus."""
        try:
            self.bus.close()
        except Exception:
            pass

