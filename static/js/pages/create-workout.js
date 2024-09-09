import { showElement, hideElement } from "../core/utils.js";
import { handleRequestSubmit } from "../core/requests.js";

/**
 * @typedef {object} Exercise
 * @property {string} value
 * @property {string} text
 * @property {string} muscle_id
 * @property {string} equipment_id
 *
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
const MUSCLE_SELECT_ID = "muscle-select-id";
const EQUIPMENT_SELECT_ID = "equipment-select-id";
const SEARCH_EXERCISE_INPUT_ID = "search-exercise-input-id";
const EXERCISE_SELECT_BTN_CLS = ".exercise-select-btn";
const EXERCISE_SELECT_ROOT_ID = "exercises-select-root";
const SELECTED_EXERCISES_ROOT_ID = "selected-exercises-id";
const CREATE_WORKOUT_BTN_ID = "create-workout-btn-id";
const EXERCISE_FORM_CARD_TEMPLATE_ID = "exercise-form-card-template-id";
const EXERCISE_FORM_CARD_CLS = ".exercise-form-card";
const EXERCISE_FORM_CARD_TITLE_CLS = ".exercise-form-card-title";
const EXERCISES_FORM_CARD = {
  CLS: ".exercise-form-card",
  CLOSE_BTN_CLS: ".exercise-form-card-close-btn",
  HEADER_CLS: ".exercise-form-card-header",
  TITLE_CLS: ".exercise-form-card-title",
};

const CREATE_WORKOUT_ERROR_ALERT_ID = "create-workout-errors-alert-id";

const TEMPLATES = {
  EXERCISE_FORM_CARD_ID: "exercise-form-card-template-id",
  EXERCISE_SELECT_ID: "exercise-select-btn-template-id",
};

const SELECT_ALL_OPTION = "all";

/**
 * @type {Context}
 */
const CONTEXT = JSON.parse(document.getElementById("context-id").textContent);
const EXERCISE_SELECT_BTN_TEMPLATE = document.getElementById(
  TEMPLATES.EXERCISE_SELECT_ID
);
const EXERCISE_FORM_CARD_TEMPLATE = document.getElementById(
  TEMPLATES.EXERCISE_FORM_CARD_ID
);
const SELECTED_EXERCISES_ROOT = document.getElementById(
  SELECTED_EXERCISES_ROOT_ID
);
const EXERCISES_SELECT_ROOT = document.getElementById(EXERCISE_SELECT_ROOT_ID);
const MUSCLE_SELECT = document.getElementById(MUSCLE_SELECT_ID);
const EQUIPMENT_SELECT = document.getElementById(EQUIPMENT_SELECT_ID);
const SEARCH_EXERCISE_INPUT = document.getElementById(SEARCH_EXERCISE_INPUT_ID);
const CREATE_WORKOUT_BTN = document.getElementById(CREATE_WORKOUT_BTN_ID);
const CREATE_WORKOUT_ERROR_ALERT = document.getElementById(
  CREATE_WORKOUT_ERROR_ALERT_ID
);

/**
 * @param {{
 * value: string,
 * name: string
 * }}
 * @returns {HTMLButtonElement}
 */
function ExerciseSelectBtn({ value, name }) {
  const templateClone = EXERCISE_SELECT_BTN_TEMPLATE.content.cloneNode(true);
  const btn = templateClone.querySelector(EXERCISE_SELECT_BTN_CLS);
  btn.value = value;
  btn.textContent = `+ ${name}`;
  return btn;
}

/**
 * @param {{
 * name: string,
 * exerciseId: string,
 * }} props
 * @returns {HTMLDivElement}
 */
function ExerciseFormCard({ name, exerciseId }) {
  const templateClone = EXERCISE_FORM_CARD_TEMPLATE.content.cloneNode(true);
  const card = templateClone.querySelector(EXERCISES_FORM_CARD.CLS);
  card.querySelector(EXERCISES_FORM_CARD.TITLE_CLS).textContent = name;
  card.dataset.exerciseId = exerciseId;
  return card;
}

/**
 * @param {{
 * exercises: Array<Exercise>,
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
 * exercises: Array<Exercise>,
 * rootElement: HTMLElement,
 * }}
 * @returns
 */
function updateExerciseSelectRoot({ exercises, rootElement }) {
  const fragment = document.createDocumentFragment();
  exercises.forEach((exercise) => {
    const btn = ExerciseSelectBtn({
      value: exercise.value,
      name: exercise.text,
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
 * }}
 */
function filterExercisesSelectOptions({
  exercises,
  muscleId,
  equipmentId,
  searchValue,
  exerciseSelectRoot,
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
  });
}

MUSCLE_SELECT.addEventListener("change", function () {
  filterExercisesSelectOptions({
    exercises: CONTEXT.exercises,
    muscleId: MUSCLE_SELECT.value,
    equipmentId: EQUIPMENT_SELECT.value,
    searchValue: SEARCH_EXERCISE_INPUT.value,
    exerciseSelectRoot: EXERCISES_SELECT_ROOT,
  });
});

EQUIPMENT_SELECT.addEventListener("change", function () {
  filterExercisesSelectOptions({
    exercises: CONTEXT.exercises,
    muscleId: MUSCLE_SELECT.value,
    equipmentId: EQUIPMENT_SELECT.value,
    searchValue: SEARCH_EXERCISE_INPUT.value,
    exerciseSelectRoot: EXERCISES_SELECT_ROOT,
  });
});

SEARCH_EXERCISE_INPUT.addEventListener("input", function () {
  filterExercisesSelectOptions({
    exercises: CONTEXT.exercises,
    muscleId: MUSCLE_SELECT.value,
    equipmentId: EQUIPMENT_SELECT.value,
    searchValue: SEARCH_EXERCISE_INPUT.value,
    exerciseSelectRoot: EXERCISES_SELECT_ROOT,
  });
});

/** @param {MouseEvent} event  */
function onClickExerciseSelectBtn(event) {
  const exerciseValue = event.target.value;

  /** @type {Exercise} */
  const exercise = CONTEXT.exercises.find(
    (exercise) => exercise.value === exerciseValue
  );
  const card = ExerciseFormCard({
    name: exercise.text,
    exerciseId: exercise.value,
  });
  SELECTED_EXERCISES_ROOT.appendChild(card);
}

/**
 * @param {MouseEvent} event
 */
async function onClickCreateWorkoutBtn(event) {
  const url = event.target.dataset.endpoint;
  const title = document.querySelector('input[name="title"]').value;
  const description = document.querySelector(
    'textarea[name="description"]'
  ).value;
  const exercises = Array.from(
    document.querySelectorAll(EXERCISE_FORM_CARD_CLS)
  ).map((card) => {
    return {
      exercise_id: card.dataset.exerciseId,
      sets: card.querySelector('input[name="sets"]').value,
      reps: card.querySelector('input[name="reps"]').value,
      rest_period: card.querySelector('input[name="rest_period"]').value,
      weight: card.querySelector('input[name="weight"]').value,
      notes: card.querySelector('textarea[name="notes"]').value,
    };
  });
  handleRequestSubmit({
    url: url,
    method: "POST",
    body: {
      title,
      description,
      exercises,
    },
    beforeSend: async () => {
      event.target.disabled = true;
      hideElement(CREATE_WORKOUT_ERROR_ALERT);
    },
    onSuccess: async (data) => {
      event.target.disabled = false;
    },
    onError: async (data, status) => {
      console.log(data.errors);
      event.target.disabled = false;
      showElement(CREATE_WORKOUT_ERROR_ALERT);
      const errorAlertContent =
        CREATE_WORKOUT_ERROR_ALERT.querySelector(".content");
      errorAlertContent.innerHTML = "";
      errorAlertContent.textContent = data.errors;
    },
  });
}

SELECTED_EXERCISES_ROOT.addEventListener("click", function (event) {
  if (event.target.matches(EXERCISES_FORM_CARD.HEADER_CLS)) {
    event.target.closest(EXERCISES_FORM_CARD.CLS).classList.toggle("collapsed");
  } else if (event.target.matches(EXERCISES_FORM_CARD.CLOSE_BTN_CLS)) {
    event.target.closest(EXERCISES_FORM_CARD.CLS).remove();
  }
});

EXERCISES_SELECT_ROOT.addEventListener("click", function (event) {
  if (event.target.matches(EXERCISE_SELECT_BTN_CLS)) {
    onClickExerciseSelectBtn(event);
  }
});

CREATE_WORKOUT_BTN.addEventListener("click", onClickCreateWorkoutBtn);
