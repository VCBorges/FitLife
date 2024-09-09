/**
 * @param {string} name
 * @returns {string}
 */
export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/**
 * @param {string?} redirectUrl
 */
export function redirectIfApplicable(redirectUrl) {
  if (redirectUrl) {
    window.location.href = new URL(redirectUrl, window.location.origin);
  }
}

/**
 * @param {{
 * method: string,
 * body: FormData | Object<string, any>,
 * headers: object
 * }}
 * @returns {{
 * method: string,
 * headers: object,
 * body: string,
 * }}
 */
export function getRequestInit({ method, body, headers = {} }) {
  if (!(body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(body);
  }
  return {
    method,
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      ...headers,
    },
    body: body,
  };
}

/**
 * @param {{
 * url: string,
 * method: string,
 * body: Object<string, any>,
 * headers: Object<string, string>,
 * onSuccess: function,
 * onError: function
 * }}
 * @returns {Promise<any>}
 */
export async function sendRequest({
  url,
  method,
  body,
  headers = {},
  onSuccess = (data) => null,
  onError = (data, status) => null,
}) {
  const requestInit = getRequestInit({
    method,
    body,
    headers,
  });
  const response = await fetch(url, requestInit);
  const data = await response.json();
  if (response.ok) {
    return onSuccess(data);
  }
  return onError(data, response.status);
}


/**
 * @param {{
* url: string,
* method: string,
* body: FormData | Object<string, any>,
* headers: object,
* beforeSend: function,
* onSuccess: function,
* onError: function,
* }} props
* @returns {Promise<any>}
*/
export async function handleRequestSubmit({
 url,
 method,
 body,
 headers = {},
 beforeSend = async () => null,
 onSuccess = async (data) => null,
 onError = async (data, status) => null,
}) {
 beforeSend();
 await sendRequest({
   url,
   method,
   body,
   headers,
   onSuccess: async (data) => {
     onSuccess(data);
     redirectIfApplicable(data.redirect_url);
   },
   onError: async (data, status) => {
     onError(data, status);
   },
 });
}