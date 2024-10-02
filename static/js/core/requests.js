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
 * body: FormData | Object<string, any> | Null,
 * headers: object
 * }} props
 * @returns {RequestInit}
 */
export function getRequestInit({ method, body = null, headers = {} }) {
  if (!(body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(body) ? body : null;
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
 * data: Object<string, any>,
 * headers: Object<string, string>,
 * onSuccess: function(Object): void,
 * onError: function(Object, number): void,
 * }} props
 * @returns {Promise<Object>}
 */
export async function sendRequest({
  url,
  method,
  data,
  headers = {},
  onSuccess = (data) => null,
  onError = (data, status) => null,
}) {
  let requestInit;
  const isGetOrHead = ["GET", "HEAD"].includes(method.toUpperCase());
  if (isGetOrHead) {
    const searchParams = new URLSearchParams(data);
    url += `?${searchParams.toString()}`;
    requestInit = getRequestInit({
      method,
      headers,
    });
  } else {
    requestInit = getRequestInit({
      method,
      body: data,
      headers,
    });
  }
  const response = await fetch(url, requestInit);
  const responseData = await response.json();
  if (response.ok) {
    onSuccess(responseData);
    return responseData;
  }
  onError(responseData, response.status);
}

/**
 * @param {{
 * url: String,
 * method: String,
 * data: FormData | Object.<String, Any>,
 * headers: Object.<String, Any>,
 * beforeSend: Function(): Void,
 * onSuccess: Function(Object): Void,
 * onError: Function(Object, Number): Void,
 * }} props
 * @returns {Promise<Any>}
 */
export async function handleRequestSubmit({
  url,
  method,
  data = {},
  headers = {},
  beforeSend = () => {},
  onSuccess = (data) => {},
  onError = (data, status) => {},
}) {
  beforeSend();
  return await sendRequest({
    url,
    method,
    data,
    headers,
    onSuccess: (data) => {
      onSuccess(data);
      redirectIfApplicable(data.redirect_url);
    },
    onError: (data, status) => {
      onError(data, status);
    },
  });
}
