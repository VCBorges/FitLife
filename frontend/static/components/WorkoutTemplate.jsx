import React from 'react';
import { NavBar } from './NavBar';

import '../styles/WorkoutTemplate.css';

/**
 * @param {*} props
 * @param {string} props.loginEndpoint
 * @param {string} props.registerEndpoint 
 * @returns {JSX.Element}
 */
export function WorkoutTemplate({ context }) {
    return (
        <div>
            <NavBar
                logoutEndpoint={context.endpoints.logout}
                fitLifeLogo={context.images.fitLifeLogo}
            />
            <div className="template-body">

            </div>   
        </div>

    )
}