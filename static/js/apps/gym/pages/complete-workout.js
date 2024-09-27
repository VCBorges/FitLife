import {
  formToObject,
  handleFormSubmit,
  isFormValid,
} from "../../../core/forms.js";
import { handleRequestSubmit } from "../../../core/requests.js";

const COMPLETE_WORKOUT_SUBMIT_BTN_ID = "complete-workout-submit-btn";
const WORKOUT_EXERCISES_ITEM_CLS = ".workout-exercise";
const IS_COMPLETED_CHECKBOX_CLS = ".is-completed";

document
  .getElementById(COMPLETE_WORKOUT_SUBMIT_BTN_ID)
  .addEventListener("click", async function (event) {
    let isValid = true;
    const exercises = Array.from(
      document.querySelectorAll(WORKOUT_EXERCISES_ITEM_CLS)
    )
      .filter((exercise) => {
        return exercise.querySelector(IS_COMPLETED_CHECKBOX_CLS).checked;
      })
      .map((exercise) => {
        const exerciseForm = exercise.querySelector("form");
        if (!isFormValid(exerciseForm)) {
          isValid = false;
        }
        return formToObject(exerciseForm);
      });
    if (!isValid) {
      return;
    }
    await handleRequestSubmit({
      url: event.target.getAttribute("formaction"),
      method: "POST",
      body: {
        exercises: exercises,
      }
    })
  });
