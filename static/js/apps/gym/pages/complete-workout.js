import { formToObject, handleFormSubmit, isFormValid } from "../../../core/forms.js";


const COMPLETE_WORKOUT_SUBMIT_BTN_ID = "complete-workout-submit-btn";
const WORKOUT_EXERCISES_ITEM_CLS = ".workout-exercise";
const IS_COMPLETED_CHECKBOX_CLS = ".is-completed";

document
  .getElementById(COMPLETE_WORKOUT_SUBMIT_BTN_ID)
  .addEventListener("click", async function (event) {
    const exercises = Array.from(
      document.querySelectorAll(WORKOUT_EXERCISES_ITEM_CLS)
    ).map((exercise) => {
      const isCompleted = exercise.querySelector(
        IS_COMPLETED_CHECKBOX_CLS
      ).checked;
      console.log(isCompleted);
      if (isCompleted) {
        const exerciseForm = exercise.querySelector("form");
        if (!isFormValid(exerciseForm)) {
          isValid = false;
        }
        return formToObject(exerciseForm);
      }
    });
    console.log(exercises);
  });
