import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { WorkoutTemplate } from '../components/WorkoutTemplate.jsx';
import { TemplateContextProvider } from '../components/providers/TemplateContextProvider.jsx';

const root = createRoot(document.getElementById('root'));
const context = JSON.parse(document.getElementById('context-id').textContent);


root.render(
    <StrictMode>
        <TemplateContextProvider value={context}>
            <WorkoutTemplate />
        </TemplateContextProvider>
    </StrictMode>
);
