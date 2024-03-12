import React from 'react';
import { useState } from 'react';
import { BaseInput } from '../inputs/BaseInput';
import { BasetButton } from '../buttons/BaseButton';
import { makeRequest } from '../../utils/requests';

import '../../styles/userRegistrationForm.css';

/**
 * @param {object} props
 * @param {string} props.registerEndApoint
 * @returns {JSX.Element}
 */
export function UserRegisterForm({ 
    registerEndpoint,
    loginEndpoint,
}) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [birthDate, setBirthDate] = useState('');
    const [cpf, setCPF] = useState('');

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
        else if (name === 'cpf') {
            setCPF(value);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        await makeRequest({
            url: registerEndpoint,
            method: 'POST',
            body: { 
                username: email, 
                password1: password,
                password2: password2,
                first_name: firstName,
                last_name: lastName,
                birth_date: birthDate,
                cpf: cpf,
            },
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            onSuccess: (data) => {
                window.location.href = data.redirect_url
            },
            onError: (error) => {},
        })
    };

    const handleLoginBtnClick = () => {
        window.location.href = loginEndpoint;
    }

    return (
        <form onSubmit={handleSubmit}>
            <BaseInput
                label="CPF"
                type="text"
                name="cpf"
                placeholder='Enter your cpf'
                value={cpf}
                onChange={handleChange}
                required={true}
            />  
            <BaseInput
                label="Email"
                type="text"
                name="username"
                placeholder='Enter your email'
                value={email}
                onChange={handleChange}
                required={true}
                autoComplete='email'
            />
            <BaseInput
                label="Password"
                type="password"
                name="password"
                placeholder='Enter your password'
                value={password}
                onChange={handleChange}
                required={true}
                autoComplete='new-password'
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

            <div className='buttons-wrapper'>
                <BasetButton
                    type="submit"
                    classes={['btn-primary']}
                    text="Register"
                />
                <BasetButton
                    type="button"
                    classes={['btn-primary']}
                    text="Login"
                    onClick={handleLoginBtnClick}
                />
            </div>
        </form>
    );
}
