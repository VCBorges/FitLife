import React from 'react';
import { UserRegisterForm } from './forms/UserRegisterForm';

import '../styles/userRegistrationTemplate.css';

/**
 * @param {*} props
 * @param {string} props.registerEndpoint
 * @param {string} props.loginEndpoint
 * @returns {JSX.Element}
 */
export function UserRegisterTemplate({ 
    registerEndpoint,
    loginEndpoint,
    fitLifeLogo,
}) {
    return (
        <div className='container-fluid'>
        <img src={fitLifeLogo} alt='FitLife Logo' className='fitlife-logo' />
            <div className='form-container col-lg-4'>
                <UserRegisterForm
                    registerEndpoint={registerEndpoint}
                    loginEndpoint={loginEndpoint}    
                />
            </div>
        </div>    
    )
}