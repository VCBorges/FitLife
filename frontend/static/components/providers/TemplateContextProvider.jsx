import React from 'react';

export const TemplateContext = React.createContext();

/**
 * ContextProvider
 * @param {Object} props
 * @param {Object} props.children
 * @param {Object} props.value
 */
export function TemplateContextProvider({ 
    children, 
    value,
 }){
    return (
        <TemplateContext.Provider value={value}>
            {children}
        </TemplateContext.Provider>
    );
};
