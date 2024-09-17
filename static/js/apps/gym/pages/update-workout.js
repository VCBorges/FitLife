import {
  SELECTED_EXERCISES_ROOT_ID,
  EXERCISE_SELECT_ROOT_ID,
  SUBMIT_WORKOUT_BTN_ID,
  MUSCLE_SELECT_ID,
  EQUIPMENT_SELECT_ID,
  SEARCH_EXERCISE_INPUT_ID,
  EXERCISE_SELECT_BTN_CLS,
  TEMPLATES,
  handleClickSelectedExercisesRoot,
  handleClickExerciseSelectRoot,
  submitWorkout,
  filterExercisesSelectOptions as filterExercisesOptions,
} from "../submitWorkouts.js";
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

const CONTEXT = JSON.parse(document.getElementById("context-id").textContent);

// SUBMIT_WORKOUT_BTN.addEventListener("click", submitWorkout);

SELECTED_EXERCISES_ROOT.addEventListener("click", function (event) {
  handleClickSelectedExercisesRoot(event);
});

EXERCISES_SELECT_ROOT.addEventListener("click", function (event) {
  handleClickExerciseSelectRoot({
    event,
    exercises: CONTEXT.exercises,
    selectedExercisesRoot: SELECTED_EXERCISES_ROOT,
    exerciseFormCardTemplate: EXERCISE_FORM_CARD_TEMPLATE,
  });
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
