import { useEffect, type JSX } from "react";
import styles from "./Camera.module.css"
import { cameraKeyboardListener } from "./keyboardListenerEffect";
import { APP_CONFIG } from "../../app/configSlice";
import { useMoveMutation, CameraDirection } from "./cameraApiSlice";


export const Camera = (): JSX.Element => {
    const [moveCamera] = useMoveMutation();

    useEffect(() => {
        const unsubscribe = cameraKeyboardListener((e) => {
            switch (e.key) {
                case "ArrowUp":
                    moveCamera(CameraDirection.UP);
                    break;
                case "ArrowDown":
                    moveCamera(CameraDirection.DOWN);
                    break;
                case "ArrowLeft":
                    moveCamera(CameraDirection.LEFT);
                    break;
                case "ArrowRight":
                    moveCamera(CameraDirection.RIGHT);
                    break;
            }
        });

        return unsubscribe;
    }, []);

    return (
        <div>
            <img className={styles.stream} src={APP_CONFIG.streamUrl} />
        </div>
    );
}
