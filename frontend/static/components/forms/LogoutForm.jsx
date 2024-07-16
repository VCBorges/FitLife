import React from 'react';
import { BaseButton } from '../buttons/BaseButton';
import { getCookie } from '../../utils/requests';




export function LogoutForm({
    logoutEndpoint,
}) {
    return (
        <form
            method="POST"
            action={logoutEndpoint}
        >
            <input type="hidden" name="csrfmiddlewaretoken" value={getCookie('csrftoken')} />
            <BaseButton
                type="submit"
                classes={['btn-primary']}
                text="Logout"
            />
        </form>
    );
}