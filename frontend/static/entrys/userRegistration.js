import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { UserRegisterForm } from '../components/forms/UserRegisterForm.jsx';

const root = createRoot(document.getElementById('root'));
const endpoints = JSON.parse(document.getElementById('endpoints-id').textContent);
root.render(
    <StrictMode>
        <UserRegisterForm
            endpoint={endpoints.register}
        />
    </StrictMode>   
);