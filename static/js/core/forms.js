import { sendRequest, redirectIfApplicable } from "./requests.js";
import { hideElement, showElement } from "./utils.js";

export const INPUT_VALIDATION_MESSAGES = {
  REQUIRED: "Please fill out this field.",
};
export const INPUT_ERRORS_CLS = ".input-errors";
export const NON_FIELD_ERRORS = "__all__";
export const ERROR_ALERT_CLS = "errors-alert";
export const SELECT_ALL_OPTION = "all";

/**
 * @param {HTMLFormElement} form
 * @returns {Object<string, any>}
 */
export function formToObject(form) {
  return Object.fromEntries(new FormData(form).entries());
}

/**
 * @param {HTMLFormElement} form
 * @returns {boolean}
 */
export function isFormValid(form) {
  if (!form.checkValidity()) {
    const inputs = form.querySelectorAll("input");
    inputs.forEach((input) => {
      if (!input.checkValidity()) {
        if (input.validationMessage === INPUT_VALIDATION_MESSAGES.REQUIRED) {
          const inputErrorsElement = input
            .closest("div")
            .querySelector(INPUT_ERRORS_CLS);
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
  const inputErrors = form.querySelectorAll(INPUT_ERRORS_CLS);
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
      const errorElement = parentElement.querySelector(INPUT_ERRORS_CLS);
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
 * beforeSend: function,
 * onSuccess: function,
 * onError: function,
 * flattenErrors: boolean
 * }} props
 */
export async function handleFormSubmit({
  event,
  beforeSend = async () => null,
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
  beforeSend();
  await sendRequest({
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
