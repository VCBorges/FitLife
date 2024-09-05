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
const EXERCISE_SELECT_BTN_CLASS = ".exercise-select-btn";
const SELECTED_EXERCISES_ROOT_ID = "selected-exercises-id";

const EXERCISE_FORM_CARD_TEMPLATE_ID = "exercise-form-card-template-id";
const EXERCISE_FORM_CARD_CLASS = ".exercise-form-card";
const EXERCISE_FORM_CARD_TITLE_CLASS = ".exercise-form-card-title";
const EXERCISES_FORM_CARD = {
  closeButtonClass: ".exercise-form-card-close-btn",
  headerClass: ".exercise-form-card-header",
};
const SELECT_ALL = "all";

/**
 * @type {Context}
 */
const CONTEXT = JSON.parse(document.getElementById("context-id").textContent);
const EXERCISE_SELECT_BTN_TEMPLATE = document.getElementById(
  "exercise-select-btn-template-id"
);
const EXERCISE_FORM_CARD_TEMPLATE = document.getElementById(
  EXERCISE_FORM_CARD_TEMPLATE_ID
);
const SELECTED_EXERCISES_ROOT = document.getElementById(
  SELECTED_EXERCISES_ROOT_ID
);
const EXERCISES_SELECT_ROOT = document.getElementById("exercises-select-root");
const MUSCLE_SELECT = document.getElementById(MUSCLE_SELECT_ID);
const EQUIPMENT_SELECT = document.getElementById(EQUIPMENT_SELECT_ID);
const SEARCH_EXERCISE_INPUT = document.getElementById(SEARCH_EXERCISE_INPUT_ID);

/**
 * @param {{
 * value: string,
 * name: string
 * }}
 * @returns {HTMLButtonElement}
 */
function ExerciseSelectBtn({ value, name }) {
  const templateClone = EXERCISE_SELECT_BTN_TEMPLATE.content.cloneNode(true);
  const btn = templateClone.querySelector(EXERCISE_SELECT_BTN_CLASS);
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
  const card = templateClone.querySelector(EXERCISE_FORM_CARD_CLASS);
  card.querySelector(EXERCISE_FORM_CARD_TITLE_CLASS).textContent = name;
  card.dataset.exerciseId = exerciseId;
  const header = card.querySelector(EXERCISES_FORM_CARD.headerClass);
  header.addEventListener("click", function () {
    const card = this.parentElement;
    card.classList.toggle("collapsed");
  });
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
      selectedMuscleId === SELECT_ALL ||
      exercise.muscle_id === selectedMuscleId;

    const isEquipmentMatch =
      selectedEquipmentId === SELECT_ALL ||
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

document
  .getElementById(MUSCLE_SELECT_ID)
  .addEventListener("change", function () {
    filterExercisesSelectOptions({
      exercises: CONTEXT.exercises,
      muscleId: MUSCLE_SELECT.value,
      equipmentId: EQUIPMENT_SELECT.value,
      searchValue: SEARCH_EXERCISE_INPUT.value,
      exerciseSelectRoot: EXERCISES_SELECT_ROOT,
    });
  });

document
  .getElementById(EQUIPMENT_SELECT_ID)
  .addEventListener("change", function () {
    filterExercisesSelectOptions({
      exercises: CONTEXT.exercises,
      muscleId: MUSCLE_SELECT.value,
      equipmentId: EQUIPMENT_SELECT.value,
      searchValue: SEARCH_EXERCISE_INPUT.value,
      exerciseSelectRoot: EXERCISES_SELECT_ROOT,
    });
  });

document
  .getElementById(SEARCH_EXERCISE_INPUT_ID)
  .addEventListener("input", function () {
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

document.addEventListener("click", function (event) {
  if (event.target.matches(EXERCISE_SELECT_BTN_CLASS)) {
    onClickExerciseSelectBtn(event);
  } else if (event.target.matches(EXERCISES_FORM_CARD.closeButtonClass)) {
    event.target.closest(EXERCISE_FORM_CARD_CLASS).remove();
  }
});
