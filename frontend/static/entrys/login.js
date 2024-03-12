import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { LoginTemplate } from '../components/loginTemplate.jsx';

const root = createRoot(document.getElementById('root'));
const endpoints = JSON.parse(document.getElementById('endpoints-id').textContent);
const images = JSON.parse(document.getElementById('images-id').textContent);

root.render(
    <StrictMode>
        <LoginTemplate
            loginEndpoint={endpoints.login}
            registerEndpoint={endpoints.register}
            fitLifeLogo={images.fitlifeLogo}
        />
    </StrictMode>
);
