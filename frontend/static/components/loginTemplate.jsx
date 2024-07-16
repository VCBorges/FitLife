import React from 'react';
import { LoginForm } from './forms/LoginForm';

import '../styles/loginTemplate.css';
import { TemplateContext } from './providers/TemplateContextProvider';
/**
 * 
 * @param {*} props
 * @param {string} props.loginEndpoint
 * @param {string} props.registerEndpoint 
 * @returns {JSX.Element}
 */
export function LoginTemplate() {
    const context = React.useContext(TemplateContext);
    return (
        <div className='container-fluid'>
            <div className='form-container col-lg-4'>
                <img src={context.images.fitLifeLogo} alt='FitLife Logo' className='fitlife-logo' />
                <LoginForm/>
            </div>
        </div>    
    )
}