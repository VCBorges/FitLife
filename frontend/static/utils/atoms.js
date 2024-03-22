import { atom } from 'jotai';

/**
 * @returns {{value: string, error: string}}
 */
export function createFormStateKey(){
    return {
        value: '',
        error: '',
    }
}

/**
 * @param {Array.<string>} formKeys
 * @returns {Object.<string, {value: string, error: string}>}
 */
export function createFormStateAtom(formKeys){
    const formState = {};
    formKeys.forEach((key) => {
        formState[key] = createFormStateKey();
    });
    return atom(formState);
}


/**
 * @param {Event} event
 * @param {function} setStateAction
 * @returns {void}
 */
export function handleFormInputChange({ event, setStateAction }){
    const { name, value } = event.target;
    setStateAction((oldState) => ({
        ...oldState,
        [name]: {
            ...oldState[name],
            value,
        },
    }));
}


/**
 * @param {Object.<string, Array.<string>>} errors
 * @param {function} setStateAction
 * @returns {void}
 */
export function handleFormErrors({ errors, setStateAction }){
    Object.keys(errors).forEach((key) => {
        setStateAction((oldState) => ({
            ...oldState,
            [key]: {
                ...oldState[key],
                error: errors[key],
            },
        }));
    });
}