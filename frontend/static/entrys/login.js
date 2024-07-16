import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { LoginTemplate } from '../components/loginTemplate.jsx';
import { TemplateContextProvider } from '../components/providers/TemplateContextProvider.jsx';

const root = createRoot(document.getElementById('root'));
const context = JSON.parse(document.getElementById('context-id').textContent);

root.render(
    <StrictMode>
        <TemplateContextProvider value={context}>
            <LoginTemplate/>
        </TemplateContextProvider>
    </StrictMode>
);
