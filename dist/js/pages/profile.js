import { handleFormSubmit } from "../core/forms.js";

const PROFILE_FORM_ID = "profile-form-id";

const PROFILE_FORM = document.getElementById(PROFILE_FORM_ID);

PROFILE_FORM.addEventListener("submit", function (event) {
  handleFormSubmit({ event });
});
