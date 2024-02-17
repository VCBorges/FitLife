import React from "react";

/**
 * @param {object} props
 * @param {string} props.type
 * @param {string[]} props.classes
 * @param {function} props.onclick
 * @param {string} props.text
 * @returns {JSX.Element}
 */
export function BasetButton({
    type,
    classes = [],
    onClick,
    text,
}) {
    classes.push('btn');
    return (
        <button
            type={type}
            className={classes.join(' ')}
            onClick={onClick}
        >
            {text}
        </button>
    );
}