import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { LoginForm } from '../components/forms/LoginForm.jsx';

const root = createRoot(document.getElementById('root'));
const endpoints = JSON.parse(document.getElementById('endpoints-id').textContent);
root.render(
    <StrictMode>
        <LoginForm
            loginEndpoint={endpoints.login}
            registerEndpoint={endpoints.register}
        />
    </StrictMode>
);
