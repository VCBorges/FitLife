import { sendRequest, redirectIfApplicable } from "./requests.js";
import { hideElement, showElement } from "./utils.js";

export const CONTROLS_VALIDATION_MESSAGES = {
  valueMissing: "Este campo é obrigatório",
  typeMismatch: "Por favor, insira um valor válido",
  patternMismatch: "Por favor, siga o formato solicitado",
  tooLong: "Por favor, reduza este texto para {maxLength} caracteres ou menos",
  tooShort: "Por favor, aumente este texto para {minLength} caracteres ou mais",
  rangeUnderflow: "Por favor, selecione um valor maior ou igual a {min}",
  rangeOverflow: "Por favor, selecione um valor menor ou igual a {max}",
  stepMismatch: "Por favor, selecione um valor válido",
  badInput: "Por favor, insira um valor válido",
  customError: "Por favor, insira um valor válido",
};
export const CONTROL_ERRORS_CLS = ".control-errors";
export const NON_FIELD_ERRORS = "__all__";
export const ERROR_ALERT_CLS = ".errors-alert";
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
    Array.from(form.elements).forEach((control) => {
      if (!control.checkValidity()) {
        const controlError = control
          .closest("div")
          .querySelector(CONTROL_ERRORS_CLS);
        controlError.textContent = control.validationMessage;
      }
    });
    return false;
  }
  return true;
}

/**
 * @param {HTMLFormElement} form
 * @returns {[boolean, Object<string, any>]}
 */
export function validateForm(form) {
  const isValid = isFormValid(form);
  if (isValid){
    const data = formToObject(form);
    return [isValid, data];
  }
  return [isValid, null];
}

/**
 * @param {{
 * form: HTMLFormElement,
 * errorAlert: HTMLElement
 * }} props
 */
function cleanFormErrors({ form, errorAlert }) {
  const inputErrors = form.querySelectorAll(CONTROL_ERRORS_CLS);
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
      const errorElement = parentElement.querySelector(CONTROL_ERRORS_CLS);
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
