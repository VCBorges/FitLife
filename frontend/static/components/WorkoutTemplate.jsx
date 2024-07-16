import React from 'react';
import { NavBar } from './NavBar';
import { TemplateContext } from './providers/TemplateContextProvider';
import { CreateWorkoutForm } from './forms/CreateWorkoutForm/CreateWorkoutForm';

import '../styles/WorkoutTemplate.css';
import { BaseSelectInput } from './selects/BaseSelectInput/BaseSelectInput';
import { WorkoutsTable } from './tables/WorkoutsTable/WorkoutsTable';

/**
 * @param {*} props
 * @param {string} props.loginEndpoint
 * @param {string} props.registerEndpoint 
 * @returns {JSX.Element}
 */
export function WorkoutTemplate() {
    const context = React.useContext(TemplateContext);

    return (
        <>
            <NavBar
                logoutEndpoint={context.endpoints.logout}
                fitLifeLogo={context.images.fitLifeLogo}
            />
            <div className="template-body">
                <WorkoutsTable workouts={context.data.user_workouts} />
                <CreateWorkoutForm
                    createWorkoutEndpoint={context.endpoints.createWorkout}
                />
            </div>   
        </>
    )
}