import React from 'react';

export function FitLifeLogo({ 
    fitLifeLogo,
    classes = [],
}) {
    classes.push('fitlife-logo');
    return (
        <img 
            src={fitLifeLogo} 
            alt='FitLife Logo' 
            className={classes.join(' ')} 
        />
    );
}