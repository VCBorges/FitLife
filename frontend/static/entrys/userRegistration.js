import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { UserRegisterForm } from '../components/forms/UserRegisterForm.jsx';

const root = createRoot(document.getElementById('root'));
root.render(
    <StrictMode>
        <UserRegisterForm/>
    </StrictMode>   
);