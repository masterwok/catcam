export function cameraKeyboardListener(handler: (e: KeyboardEvent) => void) {
    const listener = (e: KeyboardEvent) => handler(e);

    window.addEventListener("keydown", listener);

    // Return unsubscribe/cleanup function
    return () => {
        window.removeEventListener("keydown", listener);
    };
}
