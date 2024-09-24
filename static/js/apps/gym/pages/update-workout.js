import {
  SELECTED_EXERCISES_ROOT_ID,
  EXERCISE_SELECT_ROOT_ID,
  SUBMIT_WORKOUT_BTN_ID,
  MUSCLE_SELECT_ID,
  EQUIPMENT_SELECT_ID,
  SEARCH_EXERCISE_INPUT_ID,
  EXERCISE_SELECT_BTN_CLS,
  EXERCISES_FORM_CARD,
  TEMPLATES,
  WORKOUT_FORM_ID,
  handleClickExerciseSelectBtn,
  submitWorkout,
  filterExercisesSelectOptions as filterExercisesOptions,
} from "../submitWorkouts.js";
import { isFormValid, formToObject } from "../../../core/forms.js";
/**@import { Exercise } "../submitWorkouts.js" */

/**
 * @typedef {object} Muscle
 * @property {string} value
 * @property {string} text
 *
 * @typedef {object} Equipment
 * @property {string} value
 * @property {string} text
 *
 * @typedef {object} Context
 * @property {Array<Exercise>} exercises
 * @property {Array<Muscle>} muscles
 * @property {Array<Equipment>} equipment
 */

const SELECTED_EXERCISES_ROOT = document.getElementById(
  SELECTED_EXERCISES_ROOT_ID
);
const EXERCISES_SELECT_ROOT = document.getElementById(EXERCISE_SELECT_ROOT_ID);
const SUBMIT_WORKOUT_BTN = document.getElementById(SUBMIT_WORKOUT_BTN_ID);
const MUSCLE_SELECT = document.getElementById(MUSCLE_SELECT_ID);
const EQUIPMENT_SELECT = document.getElementById(EQUIPMENT_SELECT_ID);
const SEARCH_EXERCISE_INPUT = document.getElementById(SEARCH_EXERCISE_INPUT_ID);
const EXERCISE_SELECT_BTN_TEMPLATE = document.getElementById(
  TEMPLATES.EXERCISE_SELECT_ID
);
const EXERCISE_FORM_CARD_TEMPLATE = document.getElementById(
  TEMPLATES.EXERCISE_FORM_CARD_ID
);
const WORKOUT_FORM = document.getElementById(WORKOUT_FORM_ID);

/** @type {Context} */
const CONTEXT = JSON.parse(document.getElementById("context-id").textContent);

const EXERCISES_TO_DELETE = [];

SUBMIT_WORKOUT_BTN.addEventListener("click", async function (event) {
  /**@type {HTMLButtonElement} */
  const button = event.target;
  
  let isValid = true;
  if (!isFormValid(WORKOUT_FORM)) {
    isValid = false;
  }
  const workoutData = formToObject(WORKOUT_FORM);
  const exercises = Array.from(
    document.querySelectorAll(EXERCISES_FORM_CARD.CLS)
  ).map((card) => {
    const form = card.querySelector("form");
    if (!isFormValid(form)) {
      isValid = false;
    }
    return formToObject(form);
  });
  if (!isValid) {
    return;
  }
  await submitWorkout({
    submitBtn: button,
    body: {
      ...workoutData,
      exercises: {
        to_create: exercises.filter((exercise) => exercise.exercise_id),
        to_update: exercises.filter((exercise) => exercise.workout_exercise_id),
        to_delete: EXERCISES_TO_DELETE,
      },
    },
    onSuccess: () => {
      EXERCISES_TO_DELETE.length = 0;
    }
  });
});

SELECTED_EXERCISES_ROOT.addEventListener("click", function (event) {
  if (event.target.matches(EXERCISES_FORM_CARD.HEADER_CLS)) {
    event.target.closest(EXERCISES_FORM_CARD.CLS).classList.toggle("collapsed");
  } else if (event.target.matches(EXERCISES_FORM_CARD.CLOSE_BTN_CLS)) {
    const exerciseId = event.target
      .closest(EXERCISES_FORM_CARD.CLS)
      .querySelector("input[name=workout_exercise_id]").value;
      EXERCISES_TO_DELETE.push({workout_exercise_id: exerciseId});
    event.target.closest(EXERCISES_FORM_CARD.CLS).remove();
  }
});

EXERCISES_SELECT_ROOT.addEventListener("click", function (event) {
  if (event.target.matches(EXERCISE_SELECT_BTN_CLS)) {
    handleClickExerciseSelectBtn({
      event,
      exercises: CONTEXT.exercises,
      selectedExercisesRoot: SELECTED_EXERCISES_ROOT,
      exerciseFormCardTemplate: EXERCISE_FORM_CARD_TEMPLATE,
    });
  }
});

MUSCLE_SELECT.addEventListener("change", function () {
  filterExercisesOptions({
    exercises: CONTEXT.exercises,
    muscleId: MUSCLE_SELECT.value,
    equipmentId: EQUIPMENT_SELECT.value,
    searchValue: SEARCH_EXERCISE_INPUT.value,
    exerciseSelectRoot: EXERCISES_SELECT_ROOT,
    exerciseSelectBtnTemplate: EXERCISE_SELECT_BTN_TEMPLATE,
  });
});

EQUIPMENT_SELECT.addEventListener("change", function () {
  filterExercisesOptions({
    exercises: CONTEXT.exercises,
    muscleId: MUSCLE_SELECT.value,
    equipmentId: EQUIPMENT_SELECT.value,
    searchValue: SEARCH_EXERCISE_INPUT.value,
    exerciseSelectRoot: EXERCISES_SELECT_ROOT,
    exerciseSelectBtnTemplate: EXERCISE_SELECT_BTN_TEMPLATE,
  });
});

SEARCH_EXERCISE_INPUT.addEventListener("input", function () {
  filterExercisesOptions({
    exercises: CONTEXT.exercises,
    muscleId: MUSCLE_SELECT.value,
    equipmentId: EQUIPMENT_SELECT.value,
    searchValue: SEARCH_EXERCISE_INPUT.value,
    exerciseSelectRoot: EXERCISES_SELECT_ROOT,
    exerciseSelectBtnTemplate: EXERCISE_SELECT_BTN_TEMPLATE,
  });
});
