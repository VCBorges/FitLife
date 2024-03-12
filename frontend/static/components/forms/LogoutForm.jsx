import React from 'react';
import { BasetButton } from '../buttons/BaseButton';

export function LogoutForm({
    logoutEndpoint,
}) {
    return (
        <form
            method="POST"
            action={logoutEndpoint}
        >
            <input type="hidden" name="csrfmiddlewaretoken" value={getCookie('csrftoken')} />
            <BasetButton
                type="submit"
                classes={['btn-primary']}
                text="Logout"
            />
        </form>
    );
}