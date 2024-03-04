import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { UserRegisterTemplate } from '../components/UserRegisterTemplate.jsx';

const root = createRoot(document.getElementById('root'));
const endpoints = JSON.parse(document.getElementById('endpoints-id').textContent);
const images = JSON.parse(document.getElementById('images-id').textContent);
root.render(
    <StrictMode>
        <UserRegisterTemplate
            registerEndpoint={endpoints.register}
            loginEndpoint={endpoints.login}
            fitLifeLogo={images.fitlifeLogo}
        />
    </StrictMode>   
);