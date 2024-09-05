const NON_FIELD_ERRORS = "__all__";
const INPUT_ERRORS_CLASS = "input-errors";
const HIDDEN_ELEMENT_CLASS = "d-none";
const INPUT_VALIDATION_MESSAGES = {
  REQUIRED: "Please fill out this field.",
};

/**
 * @param {string} name
 * @returns {string}
 */
function getCookie(name) {
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
 * @param {HTMLElement} element
 * @returns {void}
 */
function toggleElementVisibility(element) {
  element.classList.toggle(HIDDEN_ELEMENT_CLASS);
}

/**
 * @param {HTMLElement} element
 */
function hideElement(element) {
  element.classList.add(HIDDEN_ELEMENT_CLASS);
}

/**
 * @param {HTMLElement} element
 */
function showElement(element) {
  element.classList.remove(HIDDEN_ELEMENT_CLASS);
}

/**
 * @param {string?} redirectUrl
 */
function redirectIfApplicable(redirectUrl) {
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
 * @returns {{method: string, headers: object, body: string}}
 */
function getRequestInit({ method, body, headers = {} }) {
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
async function makeRequest({
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
 *
 * @param {HTMLFormElement} form
 * @returns {boolean}
 */
function isFormValid(form) {
  if (!form.checkValidity()) {
    const inputs = form.querySelectorAll("input");
    inputs.forEach((input) => {
      if (!input.checkValidity()) {
        if (input.validationMessage === INPUT_VALIDATION_MESSAGES.REQUIRED) {
          const inputErrorsElement = input
            .closest("div")
            .querySelector(".input-errors");
          inputErrorsElement.textContent = "This field is required";
        }
      }
    });
    return false;
  }
  return true;
}

/**
 * @param {{
 * form: HTMLFormElement,
 * errorAlert: HTMLElement
 * }} props
 */
function cleanFormErrors({ form, errorAlert }) {
  const inputErrors = form.querySelectorAll(`.${INPUT_ERRORS_CLASS}`);
  inputErrors.forEach((errorMessage) => {
    if (errorMessage) {
      errorMessage.innerHTML = "";
    }
  });
  if (errorAlert) {
    errorAlert.innerHTML = "";
    hideElement(errorAlert);
  }
}

/**
 * @param {{
 * form: HTMLFormElement,
 * data: Object<string, any>,
 * errorAlert: HTMLElement,
 * flattenErrors: boolean
 * }} props
 */
function handleFormErrors({ form, data, errorAlert, flattenErrors = false }) {
  for (const [field, error] of Object.entries(data.errors)) {
    const inputElement = form.querySelector(`input[name="${field}"]`);
    if (inputElement) {
      const parentElement = inputElement.parentElement;
      const errorElement = parentElement.querySelector(
        `.${INPUT_ERRORS_CLASS}`
      );
      errorElement.textContent = error;
    } else {
      errorAlert.textContent = error;
      showElement(errorAlert);
    }
  }
}

/**
 * @param {{
 * event: Event,
 * onSuccess: function,
 * onError: function,
 * flattenErrors: boolean
 * }} props
 */
async function handleFormSubmit({
  event,
  onSuccess = async (data) => null,
  onError = async (data, status) => null,
  flattenErrors = false,
}) {
  event.preventDefault();
  const form = event.target;
  if (!isFormValid(form)) {
    return;
  }
  const formData = new FormData(form);
  const url = form.action;
  const method = form.method;
  const errorAlert = form.querySelector(form.dataset.errorsAlert);
  cleanFormErrors({
    form,
    errorAlert,
  });
  await makeRequest({
    url,
    method,
    body: formData,
    onSuccess: async (data) => {
      onSuccess(data);
      redirectIfApplicable(data.redirect_url);
    },
    onError: async (data, status) => {
      handleFormErrors({
        form,
        data,
        errorAlert,
        flattenErrors,
      });
      onError(data, status);
    },
  });
}
