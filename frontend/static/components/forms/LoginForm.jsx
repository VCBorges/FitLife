import React from 'react';
import { BaseInput } from '../inputs/BaseInput';
import { BaseButton } from '../buttons/BaseButton';
import { makeRequest } from '../../utils/requests';
import { useAtom } from 'jotai';

import { 
    createFormStateAtom, 
    handleFormInputChange, 
    handleFormErrors, 
} from '../../utils/atoms';


import '../../styles/loginForm.css';


const loginFormAtom = createFormStateAtom([
    'username',
    'password',
    '__all__',
]);



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
        handleFormInputChange({ 
            event: e, 
            setStateAction: setLoginState, 
        });
    };


    const handleSubmit = async (e) => {
        e.preventDefault();
        e.stopPropagation();

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
                handleFormErrors({ 
                    errors, 
                    setStateAction: setLoginState, 
                });
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
                placeholder='Digite seu email'
                value={loginState.username.value}
                onChange={handleChange}
                required={true}
                errorMessage={loginState.username.error}
            />
            <BaseInput
                label="Senha"
                type="password"
                name="password"
                placeholder='Digite sua senha'
                value={loginState.password.value}
                onChange={handleChange}
                required={true}
                errorMessage={loginState.password.error}
            />
            <div className='base-input-error-message'>
                {loginState.__all__.error}
            </div>
            <div className='buttons-wrapper'>
                <BaseButton
                    type="submit"
                    classes={['btn-primary', 'btn-blue']}
                    text="Login"
                />
                <BaseButton
                    type="button"
                    classes={['btn-primary', 'btn-blue']}
                    text="Registrar-se"
                    onClick={handleRegistrationBtnClick}
                />
            </div>
        </form>
    );
}
