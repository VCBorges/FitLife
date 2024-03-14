import React from 'react';
import { useState, useRef } from 'react';
import { BaseInput } from '../inputs/BaseInput';
import { BasetButton } from '../buttons/BaseButton';
import { makeRequest } from '../../utils/requests';
import { atom, useAtom } from 'jotai';

import '../../styles/loginForm.css';

const loginFormAtom = atom({
    username: {
        value: '',
        error: '',
    },
    password: {
        value: '',
        error: '',
    },
    __all__: {
        value: '',
        error: '',
    },
});

/**
 * @param {object} props
 * @param {string} props.endpoint
 * @returns {JSX.Element}
 */
export function LoginForm({ 
    loginEndpoint,
    registerEndpoint,
}) {
    const [loginState, setLoginState] = useAtom(loginFormAtom);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setLoginState((oldState) => ({
            ...oldState,
            [name]: {
                ...oldState[name],
                value,
            },
        }));
    };

    const handleErrors = (errors) => {
        Object.keys(errors).forEach((key) => {
            setLoginState((oldState) => ({
                ...oldState,
                [key]: {
                    ...oldState[key],
                    error: errors[key],
                },
            }));
        }
        );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        e.stopPropagation();
        // if (!formRef.current.checkValidity()) {}
        // formRef.current.classList.add('was-validated');

        // const form = formRef.current;
        // form.addEventListener('submit', handleSubmit);

        await makeRequest({
            url: loginEndpoint,
            method: 'POST',
            body: { 
                username: loginState.username.value,
                password: loginState.password.value,
            },
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            onSuccess: (data) => {
                window.location.href = data.redirect_url
            },
            onError: (data) => {
                const errors = data.errors;
                handleErrors(errors);
                console.log(errors)
                console.log(loginState)
            },
        })
    };

    const handleRegistrationBtnClick = () => {
        window.location.href = registerEndpoint;
    }

    return (
        <form
            onSubmit={handleSubmit} 
            className="needs-validation"
            noValidate
        >
            <BaseInput
                label="Email"
                type="text"
                name="username"
                placeholder='Enter your email'
                value={loginState.username.value}
                onChange={handleChange}
                required={true}
                errorMessage={loginState.username.error}
            />
            <BaseInput
                label="Password"
                type="password"
                name="password"
                placeholder='Enter your password'
                value={loginState.password.value}
                onChange={handleChange}
                required={true}
                errorMessage={loginState.password.error}
            />
            <div className='base-input-error-message'>
                {loginState.__all__.error}
            </div>
            <div className='buttons-wrapper'>
                <BasetButton
                    type="submit"
                    classes={['btn-primary']}
                    text="Login"
                />
                <BasetButton
                    type="button"
                    classes={['btn-primary']}
                    text="Registration"
                    onClick={handleRegistrationBtnClick}
                />
            </div>
        </form>
    );
}
