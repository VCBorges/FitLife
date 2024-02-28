import React from 'react';
import { useState, useRef } from 'react';
import { BaseInput } from '../inputs/BaseInput';
import { BasetButton } from '../buttons/BaseButton';
import { makeRequest } from '../../utils/requests';

import '../../styles/loginForm.css';
/**
 * @param {object} props
 * @param {string} props.endpoint
 * @returns {JSX.Element}
 */
export function LoginForm({ 
    loginEndpoint,
    registerEndpoint,
}) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const formRef = useRef();

    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name === 'username') {
            setEmail(value);
        } else if (name === 'password') {
            setPassword(value);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (!formRef.current.checkValidity()) {
        }
        formRef.current.classList.add('was-validated');

        const form = formRef.current;
        form.addEventListener('submit', handleSubmit);

        await makeRequest({
            url: loginEndpoint,
            method: 'POST',
            body: { username: email, password },
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            onSuccess: (data) => {
                window.location.href = data.redirect_url
            },
            onError: (error) => {
            },
            onFinally: (data) => {
            }
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
            ref={formRef}
        >
            <BaseInput
                label="Email"
                type="text"
                name="username"
                placeholder='Enter your email'
                value={email}
                onChange={handleChange}
                required={true}
            />
            <BaseInput
                label="Password"
                type="password"
                name="password"
                placeholder='Enter your password'
                value={password}
                onChange={handleChange}
                required={true}
            />
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
