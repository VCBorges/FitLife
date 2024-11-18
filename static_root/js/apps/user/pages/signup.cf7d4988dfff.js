import { handleFormSubmit } from "../../../core/forms.js";

const SIGNUP_FORM_ID = "signup-form-id";

const SIGNUP_FORM = document.getElementById(SIGNUP_FORM_ID);

SIGNUP_FORM.addEventListener("submit", async function (event) {
  handleFormSubmit({ event });
});
