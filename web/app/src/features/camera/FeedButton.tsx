import { type JSX } from "react";
import styles from "./FeedButton.module.css";
import catMascot from '../assets/mascot.png'; 

type Props = {
    className?: string,
    onClick?: () => void;
    disabled?: boolean;
};

export const FeedButton = ({
    className,
    onClick,
    disabled = false,
}: Props): JSX.Element => {
    return (
        <button
            className={`${styles.button} ${className}`}
            onClick={onClick}
            disabled={disabled}
            aria-label="Feed the cat"
        >
            <img src={catMascot} className={styles.mascot}/>
        </button>
    );
};
