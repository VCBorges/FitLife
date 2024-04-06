import React from 'react';
import { NavBar } from './NavBar';
import { TemplateContext } from './providers/TemplateContextProvider';
import { CreateWorkoutForm } from './forms/CreateWorkoutForm/CreateWorkoutForm';

import '../styles/WorkoutTemplate.css';
import { BaseSelectInput } from './selects/BaseSelectInput/BaseSelectInput';

/**
 * @param {*} props
 * @param {string} props.loginEndpoint
 * @param {string} props.registerEndpoint 
 * @returns {JSX.Element}
 */
export function WorkoutTemplate() {
    const context = React.useContext(TemplateContext);
    console.log(context);
    return (
        <>
            <NavBar
                logoutEndpoint={context.endpoints.logout}
                fitLifeLogo={context.images.fitLifeLogo}
            />
            <div className="template-body">
                <CreateWorkoutForm
                    createWorkoutEndpoint={context.endpoints.createWorkout}
                />
            </div>   
        </>
    )
}