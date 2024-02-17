import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { LoginForm } from '../components/forms/LoginForm.jsx';

const root = createRoot(document.getElementById('root'));
root.render(
    <StrictMode>
        <LoginForm/>
    </StrictMode>
);