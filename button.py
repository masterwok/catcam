import asyncio
from gpiozero import Button, LED
from network import is_ap_mode, start_captive_portal

button = Button(4, pull_up=False, hold_time=1.0)
led = LED(27)

async def on_held():
    is_ap = await is_ap_mode()

    if(not is_ap):
        print("Entering AP mode...")
        await start_captive_portal();
        led.blink(on_time=0.5, off_time=0.5, background=True)

def on_held_async_delegate(loop: asyncio.AbstractEventLoop):
    def _delegate():
        fut = asyncio.run_coroutine_threadsafe(on_held(), loop)
        fut.add_done_callback(lambda f: f.exception())
    return _delegate

async def main():
    button.when_held = on_held_async_delegate(asyncio.get_running_loop())

    print("Waiting...")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

