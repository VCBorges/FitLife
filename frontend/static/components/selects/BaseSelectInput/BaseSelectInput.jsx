import React from "react";

import './BaseSelectInput.css'

export function BaseSelectInput({
    name,
    label,
    value,
    options,
    onChange,
    required = false,
    disabled = false,
    classes = '',
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