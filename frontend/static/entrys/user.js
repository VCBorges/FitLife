import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { UserTemplate } from '../components/UserTemplate.jsx';

const root = createRoot(document.getElementById('root'));
const context = JSON.parse(document.getElementById('context-id').textContent);


root.render(
    <StrictMode>
        <UserTemplate
            context={context}
        />
    </StrictMode>
);
