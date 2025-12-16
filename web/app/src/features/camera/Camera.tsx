import { useEffect, type JSX } from "react";
import styles from "./Camera.module.css";
import { cameraKeyboardListener } from "./keyboardListenerEffect";
import { APP_CONFIG } from "../../app/appConfig";
import { useMoveMutation, CameraDirection } from "./cameraApiSlice";
import { FeedButton } from "./FeedButton";

const feed = () => {

}

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
    }, [moveCamera]);

    return (
        <div className={styles.cameraContainer}>
            <img
                className={styles.stream}
                src={APP_CONFIG.streamUrl}
                alt="Cat camera live stream"
            />

            <FeedButton className={styles.feedButton} onClick={feed} />

            <button
                type="button"
                className={`${styles.tapZone} ${styles.top}`}
                aria-label="Pan camera up"
                onClick={() => moveCamera(CameraDirection.UP)}
            />

            <button
                type="button"
                className={`${styles.tapZone} ${styles.bottom}`}
                aria-label="Pan camera down"
                onClick={() => moveCamera(CameraDirection.DOWN)}
            />

            <button
                type="button"
                className={`${styles.tapZone} ${styles.left}`}
                aria-label="Pan camera left"
                onClick={() => moveCamera(CameraDirection.LEFT)}
            />

            <button
                type="button"
                className={`${styles.tapZone} ${styles.right}`}
                aria-label="Pan camera right"
                onClick={() => moveCamera(CameraDirection.RIGHT)}
            />
        </div>
    );
};
