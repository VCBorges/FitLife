export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


/**
 * @param {object} options
 * @param {string} options.url
 * @param {string} options.method
 * @param {object} options.body
 * @param {object} options.headers
 * @returns {object}
 */
async function getResponse({url, method, body, headers}) {
    return await fetch(url, {
        method,
        body,
        headers
    });
}

/**
 * @param {object} options
 * @param {string} options.url
 * @param {string} options.method
 * @param {object} options.body
 * @param {object} options.headers
 * @param {function} options.onSuccess
 * @param {function} options.onError
 * @param {function} options.onFinally
 * @returns {object}
 */
export async function makeRequest({
    url,
    method,
    body,
    headers,
    onSuccess = () => {},
    onError = () => {},
    onFinally = () => {},
}) {
    const response = await getResponse({
        url,
        method,
        body: JSON.stringify(body),
        headers: {
            'content-type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
            ...headers
        }
    });
    
    const data = await response.json();
    if (response.ok) {
        onSuccess(data);
    }
    else {
        onError(data, response.status);
    }
    onFinally(data);
    return data;
}
