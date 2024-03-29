import React from 'react';
import { NavBar } from './NavBar';

import '../styles/userTemplate.css';

/**
 * @param {*} props
 * @param {string} props.loginEndpoint
 * @param {string} props.registerEndpoint 
 * @returns {JSX.Element}
 */
export function UserTemplate({ context }) {
    return (
        <div>
            <NavBar
                logoutEndpoint={context.endpoints.logout}
                fitLifeLogo={context.images.fitLifeLogo}
            />
            {/* <hr className='navbar-separator'/> */}
            <div className="user-template-body">

            </div>   
        </div>

    )
}