import React from 'react';
import { useState } from 'react';
import { BaseInput } from '../inputs/BaseInput';
import { BaseButton } from '../buttons/BaseButton';
import { makeRequest } from '../../utils/requests';
import { atom, useAtom } from 'jotai';

import { 
    createFormStateAtom, 
    handleFormInputChange, 
    handleFormErrors, 
} from '../../utils/atoms';


import '../../styles/userRegistrationForm.css';


const userRegisterAtom = createFormStateAtom([
    'username',
    'password',
    'password2',
    'first_name',
    'last_name',
    'birth_date',
    'cpf',
]);

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
        handleFormInputChange({ 
            event: e, 
            setStateAction: setUserState, 
        });
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
                    handleFormErrors({
                        errors: data.errors,
                        setStateAction: setUserState,
                    });
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
                placeholder='Digite seu CPF'
                value={userState.cpf.value}
                onChange={handleChange}
                required={true}
                errorMessage={userState.cpf.error}
            />  
            <BaseInput
                label="Email"
                type="text"
                name="username"
                placeholder='Digite seu email'
                value={userState.username.value}
                onChange={handleChange}
                required={true}
                autoComplete='email'
                errorMessage={userState.username.error}
            />
            <BaseInput
                label="Senha"
                type="password"
                name="password"
                placeholder='Digite sua senha'
                value={userState.password.value}
                onChange={handleChange}
                required={true}
                autoComplete='new-password'
                errorMessage={userState.password.error}
            />
            <BaseInput
                label="Confirmar Senha"
                type="password"
                name="password2"
                placeholder='Confirme sua senha'
                value={userState.password2.value}
                onChange={handleChange}
                required={true}
                errorMessage={userState.password2.error}
            />
            <BaseInput
                label="Primeiro Nome"
                type="text"
                name="first_name"
                placeholder='Digite seu primeiro nome'
                value={userState.first_name.value}
                onChange={handleChange}
                required={true}
                errorMessage={userState.first_name.error}
            />
            <BaseInput
                label="Sobrenome"
                type="text"
                name="last_name"
                placeholder='Digite seu sobrenome'
                value={userState.last_name.value}
                onChange={handleChange}
                required={true}
                errorMessage={userState.last_name.error}
            />
            <BaseInput
                label="Data de Nascimento"
                type="date"
                name="birth_date"
                placeholder='Digite sua data de nascimento'
                value={userState.birth_date.value}
                onChange={handleChange}
                required={true}
                errorMessage={userState.birth_date.error}
            />

            <div className='buttons-wrapper'>
                <BaseButton
                    type="submit"
                    classes={['btn-primary']}
                    text="Cadastrar"
                />
                <BaseButton
                    type="button"
                    classes={['btn-primary']}
                    text="Ir para Login"
                    onClick={handleLoginBtnClick}
                />
            </div>
        </form>
    );
}
