import React from "react";

import './BaseSelectInput.css'

/**
 * BaseSelectInput component
 * @param {{
 * name: string,
 * label: string,
 * value: string,
 * options: {value: string, label: string}[],
 * onChange: (event: React.ChangeEvent<HTMLSelectElement>) => void,
 * required: boolean,
 * disabled: boolean,
 * classes: string,
 * register: function,
 * }} props
 * @returns {JSX.Element}
 */
export function BaseSelectInput({
    name,
    label,
    value,
    options,
    onChange,
    required = false,
    disabled = false,
    classes = '',
    register,
}) {
    return (
        <div className="form-group base-select-label">
            <label htmlFor={name}>{label}</label>
            <select
                className={`form-control base-select ${classes}`}
                name={name}
                id={name}
                value={value}
                onChange={onChange}
                required={required}
                disabled={disabled}
                {...register(name, {required: required})}
            >
                {options.map((option, index) => {
                    return (
                        <option key={index} value={option.value}>
                            {option.label}
                        </option>
                    );
                })}
            </select>
        </div>
    );
}