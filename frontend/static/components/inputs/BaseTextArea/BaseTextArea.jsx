import React from 'react'

import './BaseTextArea.css'


export function BaseTextArea({
    label,
    name,
    placeholder,
    value,
    onChange = () => {},
    classes = [],
    readOnly = false,
    required = false,
    autoComplete = '',
    errorMessage = '',
    register,
}) {
    classes.push('form-control')
    classes.push('base-text-area')
    return (
        <div>
            <label
                className='base-text-area-label'
                htmlFor={name}>{label}
            </label>
            <textarea
                className={classes.join(' ')}
                id={name}
                name={name}
                value={value}
                placeholder={placeholder}
                onChange={onChange}
                readOnly={readOnly}
                required={required}
                autoComplete={autoComplete}
                {...register(name, {
                    required: required
                })}
            />
            <div className='base-text-area-error-message'>
                {errorMessage}
            </div>
        </div>
    )
}