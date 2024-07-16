import React from 'react';

import '../../styles/baseInput.css';
/**
 * @param {{
 *      label: string,
 *      type: string,
 *      name: string,   
 *      placeholder: string,
 *      value: string,
 *      onChange: function,
 *      classes: string[],
 *      readOnly: boolean,
 *      required: boolean,
 *      autoComplete: string,
 *      errorMessage: string,
 *      register: function
 * }} props
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
    register = () => {},
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
                autoComplete={autoComplete}
                {...register(name, {
                    required: {
                        value: required,
                        message: `O campo ${label.toLowerCase()} é obrigatório`
                    }
                })}
            />
            <div className='base-input-error-message'>
                {errorMessage}
            </div>
        </div>
    );
}