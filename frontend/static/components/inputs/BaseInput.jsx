import React from 'react';

import '../../styles/baseInput.css';
/**
 * BaseInput
 * @param {object} props
 * @param {string} props.label
 * @param {string} props.type
 * @param {string} props.name
 * @param {string} props.placeholder
 * @param {string} props.value
 * @param {function} props.onChange
 * @param {string[]} props.classes
 * @param {boolean} props.readOnly
 * @param {boolean} props.required
 * @param {string} props.autoComplete
 * @returns {JSX.Element}
 */
export function BaseInput({ 
    label,
    type, 
    name,
    placeholder,
    value, 
    onChange = () => {},
    classes = [],
    readOnly = false,
    required = false,
    autoComplete = '',
    errorMessage = '',
    // ref = null
}) {
    classes.push('form-control');
    classes.push('base-input');
    // classes.push('is-invalid');
    return (
        <div>
            <label 
                className='base-input-label' 
                htmlFor={name}>{label}
            </label>
            <input 
                className={classes.join(' ')} 
                type={type} 
                id={name} 
                name={name} 
                value={value}
                placeholder={placeholder} 
                onChange={onChange} 
                readOnly={readOnly}
                required={required}
                autoComplete={autoComplete}
                // ref={ref}
            />
            <div className='base-input-error-message'>
                {errorMessage}
            </div>
        </div>
    );
}