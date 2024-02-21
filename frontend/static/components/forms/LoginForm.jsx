import React from 'react';
import { useState } from 'react';
import { BaseInput } from '../inputs/BaseInput';
import { BasetButton } from '../buttons/BaseButton';
import { makeRequest } from '../../utils/requests';

/**
 * @param {object} props
 * @param {string} props.endpoint
 * @returns {JSX.Element}
 */
export function LoginForm({ endpoint }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

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

        await makeRequest({
            url: endpoint,
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
                console.log('Finally');
                console.log(data);
            }
        })
    };

    const handleRegistrationBtnClick = () => {
        window.location.href = '/users/register/'
    }

    return (
        <form onSubmit={handleSubmit}>
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
        </form>
    );
}
