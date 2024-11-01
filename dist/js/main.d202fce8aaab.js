import { handleFormSubmit } from "./core/forms.js";

const LOGOUT_FORM_ID = "logout-form-id";

const LOGOUT_FORM = document.getElementById(LOGOUT_FORM_ID);

if (LOGOUT_FORM) {
  LOGOUT_FORM.addEventListener("submit", function (event) {
    handleFormSubmit({ event });
  });
}