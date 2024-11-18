import {
  formToObject,
  handleFormSubmit,
  isFormValid,
} from "../../../core/forms.js";
import { handleRequestSubmit } from "../../../core/requests.js";

/**
 * @typedef {Object} CompleteWorkoutExercise
 * @property {String} workout_exercise_id
 * @property {Boolean?} is_done
 * @property {Number} repetitions
 * @property {Number} sets
 * @property {Number} weight
 * @property {Number} rest_period
 */

const COMPLETE_WORKOUT_SUBMIT_BTN_ID = "complete-workout-submit-btn";
const WORKOUT_EXERCISES_ITEM_CLS = ".workout-exercise";

document
  .getElementById(COMPLETE_WORKOUT_SUBMIT_BTN_ID)
  .addEventListener("click", async function (event) {
    let isValid = true;

    /**@type {CompleteWorkoutExercise[]?} */
    const exercises = Array.from(
      document.querySelectorAll(WORKOUT_EXERCISES_ITEM_CLS)
    ).map((exercise) => {
      /**@type {HTMLFormElement} */
      const exerciseForm = exercise.querySelector("form");
      if (!isFormValid(exerciseForm)) {
        isValid = false;
      }
      return formToObject(exerciseForm);
    });
    if (!isValid || exercises.length === 0) {
      return;
    }
    console.log(exercises);
    await handleRequestSubmit({
      url: event.target.getAttribute("formaction"),
      method: "POST",
      data: {
        workout_id: event.target.value,
        exercises: exercises,
      },
    });
  });
