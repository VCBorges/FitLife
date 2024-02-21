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
export function UserRegisterForm({ endpoint }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [birthDate, setBirthDate] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name === 'username') {
            setEmail(value);
        } else if (name === 'password') {
            setPassword(value);
        }
        else if (name === 'password2') {
            setPassword2(value);
        }
        else if (name === 'first_name') {
            setFirstName(value);
        }
        else if (name === 'last_name') {
            setLastName(value);
        }
        else if (name === 'birth_date') {
            setBirthDate(value);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        await makeRequest({
            url: endpoint,
            method: 'POST',
            body: { 
                username: email, 
                password1: password,
                password2: password2,
                first_name: firstName,
                last_name: lastName,
                birth_date: birthDate,
            },
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            onSuccess: (data) => {
                window.location.href = data.redirect_url
            },
            onError: (error) => {
            },
        })
    };

    const handleRegistrationBtnClick = () => {
        window.location.href = '/login/'
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
            <BaseInput
                label="Password"
                type="password"
                name="password2"
                placeholder='Enter your password'
                value={password2}
                onChange={handleChange}
                required={true}
            />
            <BaseInput
                label="First Name"
                type="text"
                name="first_name"
                placeholder='Enter your first name'
                value={firstName}
                onChange={handleChange}
                required={true}
            />
            <BaseInput
                label="Last Name"
                type="text"
                name="last_name"
                placeholder='Enter your last name'
                value={lastName}
                onChange={handleChange}
                required={true}
            />
            <BaseInput
                label="Birth Date"
                type="date"
                name="birth_date"
                placeholder='Enter your birth date'
                value={birthDate}
                onChange={handleChange}
                required={true}
            />
            <BasetButton
                type="submit"
                classes={['btn-primary']}
                text="Register"
            />
            <BasetButton
                type="button"
                classes={['btn-primary']}
                text="Login"
                onClick={handleRegistrationBtnClick}
            />
        </form>
    );
}
