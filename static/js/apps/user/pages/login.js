import { handleFormSubmit } from "../../../core/forms.js";

const LOGIN_FORM_ID = "login-form-id";

const LOGIN_FORM = document.getElementById(LOGIN_FORM_ID);

LOGIN_FORM.addEventListener("submit", async function (event) {
  handleFormSubmit({ event });
});
