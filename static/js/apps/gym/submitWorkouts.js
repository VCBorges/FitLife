import { showElement, hideElement } from "../../core/utils.js";
import { handleRequestSubmit } from "../../core/requests.js";
import { isFormValid, formToObject } from "../../core/forms.js";

/**
 * @typedef {object} Exercise
 * @property {string} value
 * @property {string} text
 * @property {string} muscle_id
 * @property {string} equipment_id
 */
export const MUSCLE_SELECT_ID = "muscle-select-id";
export const EQUIPMENT_SELECT_ID = "equipment-select-id";
export const SEARCH_EXERCISE_INPUT_ID = "search-exercise-input-id";
export const EXERCISE_SELECT_BTN_CLS = ".exercise-select-btn";
export const EXERCISE_SELECT_ROOT_ID = "exercises-select-root";
export const SELECTED_EXERCISES_ROOT_ID = "selected-exercises-id";
export const SUBMIT_WORKOUT_BTN_ID = "submit-workout-btn-id";
export const EXERCISES_FORM_CARD = {
  CLS: ".exercise-form-card",
  CLOSE_BTN_CLS: ".exercise-form-card-close-btn",
  HEADER_CLS: ".exercise-form-card-header",
  TITLE_CLS: ".exercise-form-card-title",
};
export const WORKOUT_DATA_FORM_ID = "workout-data-form-id";
export const ERROR_ALERT_ID = "errors-alert-id";
export const TEMPLATES = {
  EXERCISE_FORM_CARD_ID: "exercise-form-card-template-id",
  EXERCISE_SELECT_ID: "exercise-select-btn-template-id",
};

const SELECT_ALL_OPTION = "all";

// TODO: Fix when the click is on the card title div the collapse does not work

/**
 * @param {{
 * value: string,
 * name: string
 * template: HTMLTemplateElement,
 * }}
 * @returns {HTMLButtonElement}
 */
function ExerciseSelectBtn({ value, name, template }) {
  const templateClone = template.content.cloneNode(true);
  const btn = templateClone.querySelector(EXERCISE_SELECT_BTN_CLS);
  btn.value = value;
  btn.textContent = `+ ${name}`;
  return btn;
}

/**
 * @param {{
 * name: string,
 * exerciseId: string,
 * template: HTMLTemplateElement,
 * }} props
 * @returns {HTMLDivElement}
 */
function ExerciseFormCard({ name, exerciseId, template }) {
  const templateClone = template.content.cloneNode(true);
  const card = templateClone.querySelector(EXERCISES_FORM_CARD.CLS);
  card.querySelector(EXERCISES_FORM_CARD.TITLE_CLS).textContent = name;
  const exerciseIdInput = card.querySelector("input[name=exercise_id]");
  exerciseIdInput.value = exerciseId;
  return card;
}

/**
 * @param {MouseEvent} event
 **/
export function handleClickSelectedExercisesRoot(event) {
  if (event.target.matches(EXERCISES_FORM_CARD.HEADER_CLS)) {
    event.target.closest(EXERCISES_FORM_CARD.CLS).classList.toggle("collapsed");
  } else if (event.target.matches(EXERCISES_FORM_CARD.CLOSE_BTN_CLS)) {
    event.target.closest(EXERCISES_FORM_CARD.CLS).remove();
  }
}

/**
 * @param {{
 * event: MouseEvent,
 * exercises: Exercise[],
 * selectedExercisesRoot: HTMLDivElement,
 * exerciseFormCardTemplate: HTMLTemplateElement,
 * }} props
 */
export function handleClickExerciseSelectRoot({
  event,
  exercises,
  selectedExercisesRoot,
  exerciseFormCardTemplate,
}) {
  if (event.target.matches(EXERCISE_SELECT_BTN_CLS)) {
    handleClickExerciseSelectBtn({
      event,
      exercises: exercises,
      selectedExercisesRoot: selectedExercisesRoot,
      exerciseFormCardTemplate: exerciseFormCardTemplate,
    });
  }
}

/**
 * @param {{
 * exercises: Exercise[],
 * selectedMuscleId: string,
 * selectedEquipmentId: string,
 * searchValue: string,
 * }} props
 * @returns {Array<Exercise>}
 */
function filterExercises({
  exercises,
  selectedMuscleId,
  selectedEquipmentId,
  searchValue,
}) {
  return exercises.filter((exercise) => {
    const isMuscleMatch =
      selectedMuscleId === SELECT_ALL_OPTION ||
      exercise.muscle_id === selectedMuscleId;

    const isEquipmentMatch =
      selectedEquipmentId === SELECT_ALL_OPTION ||
      exercise.equipment_id === selectedEquipmentId;

    const isSearchValueMatch =
      !searchValue ||
      exercise.text.toLowerCase().includes(searchValue.toLowerCase());

    return isMuscleMatch && isEquipmentMatch && isSearchValueMatch;
  });
}

/**
 * @param {{
 * exercises: Exercise[],
 * rootElement: HTMLElement,
 * exerciseSelectBtnTemplate: HTMLTemplateElement,
 * }}
 * @returns
 */
function updateExerciseSelectRoot({
  exercises,
  rootElement,
  exerciseSelectBtnTemplate,
}) {
  const fragment = document.createDocumentFragment();
  exercises.forEach((exercise) => {
    const btn = ExerciseSelectBtn({
      value: exercise.value,
      name: exercise.text,
      template: exerciseSelectBtnTemplate,
    });
    fragment.appendChild(btn);
  });
  rootElement.innerHTML = "";
  rootElement.appendChild(fragment);
}

/**
 * @param {{
 * exercises: Array<Exercise>,
 * muscleId: string,
 * equipmentId: string,
 * searchValue: string,
 * exerciseSelectRoot: HTMLElement,
 * exerciseSelectBtnTemplate: HTMLTemplateElement,
 * }}
 */
export function filterExercisesSelectOptions({
  exercises,
  muscleId,
  equipmentId,
  searchValue,
  exerciseSelectRoot,
  exerciseSelectBtnTemplate
}) {
  const options = filterExercises({
    exercises: exercises,
    selectedMuscleId: muscleId,
    selectedEquipmentId: equipmentId,
    searchValue: searchValue,
  });
  updateExerciseSelectRoot({
    exercises: options,
    rootElement: exerciseSelectRoot,
    exerciseSelectBtnTemplate: exerciseSelectBtnTemplate,
  });
}

/**
 * @param {{
 * event: MouseEvent,
 * exercises: Exercise[],
 * selectedExercisesRoot: HTMLDivElement,
 * exerciseFormCardTemplate: HTMLTemplateElement,
 * }} props
 * */
export function handleClickExerciseSelectBtn({
  event,
  exercises,
  selectedExercisesRoot,
  exerciseFormCardTemplate,
}) {
  const exerciseValue = event.target.value;

  /** @type {Exercise} */
  const exercise = exercises.find(
    (exercise) => exercise.value === exerciseValue
  );
  const card = ExerciseFormCard({
    name: exercise.text,
    exerciseId: exercise.value,
    template: exerciseFormCardTemplate,
  });
  selectedExercisesRoot.appendChild(card);
}

/**
 * @param {{
 * url: string,
 * method: string,
 * body: Object<String, Any>,
 * errorAlert: HTMLDivElement,
 * }} props
 */
export async function submitWorkout({ 
  method,
  url, 
  body, 
  errorAlert,
}) {
  //   const url = form.action;
  // let isValid = true;
  // if (!isFormValid(form)) {
  // isValid = false;
  // }
  // const workout = formToObject(new FormData(form));

  // const exercises = Array.from(
  //   document.querySelectorAll(EXERCISES_FORM_CARD.CLS)
  // ).map((card) => {
  //   const form = card.querySelector("form");
  //   if (!isFormValid(form)) {
  //     isValid = false;
  //   }
  //   return formToObject(form);
  // });

  // if (!isValid) {
  //   return;
  // }

  handleRequestSubmit({
    url: url,
    method: method,
    body: body,
    beforeSend: () => {
      button.disabled = true;
      hideElement(errorAlert);
    },
    onSuccess: (data) => {
      button.disabled = false;
    },
    onError: (data, status) => {
      button.disabled = false;
      showElement(errorAlert);
      const errorAlertContent = errorAlert.querySelector(".content");
      errorAlertContent.innerHTML = "";
      errorAlertContent.textContent = data.errors;
    },
  });
}
