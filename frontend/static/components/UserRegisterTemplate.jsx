import React from 'react';
import { UserRegisterForm } from './forms/UserRegisterForm';

import '../styles/userRegistrationTemplate.css';
import { TemplateContext } from './providers/TemplateContextProvider';

/**
 * @param {*} props
 * @param {string} props.registerEndpoint
 * @param {string} props.loginEndpoint
 * @returns {JSX.Element}
 */
export function UserRegisterTemplate() {
    const context = React.useContext(TemplateContext);

    return (
        <div className='container-fluid'>
        <img src={context.images.fitLifeLogo} alt='FitLife Logo' className='fitlife-logo' />
            <div className='form-container col-lg-4'>
                <UserRegisterForm />
            </div>
        </div>    
    )
}