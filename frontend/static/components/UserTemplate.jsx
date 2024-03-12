import React from 'react';
import { NavBar } from './NavBar';

/**
 * 
 * @param {*} props
 * @param {string} props.loginEndpoint
 * @param {string} props.registerEndpoint 
 * @returns {JSX.Element}
 */
export function UserTemplate({ context }) {
    return (
        <NavBar
            logoutEndpoint={context.endpoints.logout}
            fitLifeLogo={context.images.fitLifeLogo}
        />    
    )
}