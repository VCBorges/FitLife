import React from 'react';
import { LoginForm } from './forms/LoginForm';

import '../styles/loginTemplate.css';
/**
 * 
 * @param {*} props
 * @param {string} props.loginEndpoint
 * @param {string} props.registerEndpoint 
 * @returns {JSX.Element}
 */
export function LoginTemplate({ 
    loginEndpoint, 
    registerEndpoint,
    fitLifeLogo,
}) {
    return (
        <div className='container-fluid'>
            <div className='form-container col-lg-4'>
                <img src={fitLifeLogo} alt='FitLife Logo' className='fitlife-logo' />
                <LoginForm
                    loginEndpoint={loginEndpoint}
                    registerEndpoint={registerEndpoint}    
                />
            </div>
        </div>    
    )
}