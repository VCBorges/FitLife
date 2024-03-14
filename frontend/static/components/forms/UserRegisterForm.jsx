import React from 'react';
import { useState } from 'react';
import { BaseInput } from '../inputs/BaseInput';
import { BasetButton } from '../buttons/BaseButton';
import { makeRequest } from '../../utils/requests';
import { atom, useAtom } from 'jotai';

import '../../styles/userRegistrationForm.css';


const userRegisterAtom = atom({
    username: {
        value: '',
        error: '',
    },
    password: {
        value: '',
        error: '',
    },
    password2: {
        value: '',
        error: '',
    },
    first_name: {
        value: '',
        error: '',
    },
    last_name: {
        value: '',
        error: '',
    },
    birth_date: {
        value: '',
        error: '',
    },
    cpf: {
        value: '',
        error: '',
    },
});

/**
 * @param {object} props
 * @param {string} props.registerEndApoint
 * @returns {JSX.Element}
 */
export function UserRegisterForm({ 
    registerEndpoint,
    loginEndpoint,
}) {
    const [userState, setUserState] = useAtom(userRegisterAtom);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUserState((oldState) => ({
            ...oldState,
            [name]: {
                ...oldState[name],
                value,
            },
        }));
    };

    const handleErrors = (errors) => {
        Object.keys(errors).forEach((key) => {
            setUserState((oldState) => ({
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

        await makeRequest({
            url: registerEndpoint,
            method: 'POST',
            body: { 
                username: userState.username.value, 
                password1: userState.password.value,
                password2: userState.password2.value,
                first_name: userState.first_name.value,
                last_name: userState.last_name.value,
                birth_date: userState.birth_date.value,
                cpf: userState.cpf.value,
            },
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            onSuccess: (data) => {
                window.location.href = data.redirect_url
            },
            onError: (data, status) => {
                if (status === 400) {
                    handleErrors(data.errors);
                }
            },
        })
    };

    const handleLoginBtnClick = () => {
        window.location.href = loginEndpoint;
    }

    return (
        <form 
            onSubmit={handleSubmit} 
            className="needs-validation"
            noValidate
        >
            <BaseInput
                label="CPF"
                type="text"
                name="cpf"
                placeholder='Enter your cpf'
                value={userState.cpf.value}
                onChange={handleChange}
                required={true}
                errorMessage={userState.cpf.error}
            />  
            <BaseInput
                label="Email"
                type="text"
                name="username"
                placeholder='Enter your email'
                value={userState.username.value}
                onChange={handleChange}
                required={true}
                autoComplete='email'
                errorMessage={userState.username.error}
            />
            <BaseInput
                label="Password"
                type="password"
                name="password"
                placeholder='Enter your password'
                value={userState.password.value}
                onChange={handleChange}
                required={true}
                autoComplete='new-password'
                errorMessage={userState.password.error}
            />
            <BaseInput
                label="Password"
                type="password"
                name="password2"
                placeholder='Enter your password'
                value={userState.password2.value}
                onChange={handleChange}
                required={true}
                errorMessage={userState.password2.error}
            />
            <BaseInput
                label="First Name"
                type="text"
                name="first_name"
                placeholder='Enter your first name'
                value={userState.first_name.value}
                onChange={handleChange}
                required={true}
                errorMessage={userState.first_name.error}
            />
            <BaseInput
                label="Last Name"
                type="text"
                name="last_name"
                placeholder='Enter your last name'
                value={userState.last_name.value}
                onChange={handleChange}
                required={true}
                errorMessage={userState.last_name.error}
            />
            <BaseInput
                label="Birth Date"
                type="date"
                name="birth_date"
                placeholder='Enter your birth date'
                value={userState.birth_date.value}
                onChange={handleChange}
                required={true}
                errorMessage={userState.birth_date.error}
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
