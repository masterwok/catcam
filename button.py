from gpiozero import Button, LED
from signal import pause

# Button on GPIO4; LED on GPIO27
button = Button(4, pull_up=False, hold_time=2.0)
led = LED(27)

def on_held():
    print("Button held for 2 seconds!")

led.blink(on_time=0.5, off_time=0.5)
button.when_held = on_held

print("Waiting...")

# keeps the script running
pause()   
