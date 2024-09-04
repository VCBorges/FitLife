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

/**
 * @type {Context}
 */
const CONTEXT = JSON.parse(document.getElementById("context-id").textContent);
const EXERCISE_SELECT_BTN_TEMPLATE = document.getElementById(
  "exercise-select-btn-template-id"
);
const EXERCISES_SELECT_ROOT = document.getElementById("exercises-select-root");
const MUSCLE_SELECT_ID = "muscle-select-id";
const EQUIPMENT_SELECT_ID = "equipment-select-id";
const MUSCLE_SELECT = document.getElementById(MUSCLE_SELECT_ID);
const EQUIPMENT_SELECT = document.getElementById(EQUIPMENT_SELECT_ID);
const SELECT_ALL = "all";

/**
 * @param {{
 * value: string,
 * name: string
 * }}
 * @returns {Context}
 */
function ExerciseSelectBtn({ value, name }) {
  const templateClone = EXERCISE_SELECT_BTN_TEMPLATE.content.cloneNode(true);
  const btn = templateClone.querySelector(".exercise-select-btn");
  btn.value = value;
  btn.textContent = `+ ${name}`;
  return btn;
}

/**
 * @param {{
 * exercises: Array<Exercise>,
 * muscleId: string,
 * equipmentId: string
 * }}
 * @returns {Array<Exercise>}
 */
function filterExercises({ exercises, muscleId, equipmentId }) {
  return exercises.filter((exercise) => {
    const isMuscleMatch =
      muscleId === SELECT_ALL || exercise.muscle_id === muscleId;
    const isEquipmentMatch =
      equipmentId === SELECT_ALL || exercise.equipment_id === equipmentId;
    return isMuscleMatch && isEquipmentMatch;
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

document
  .getElementById(MUSCLE_SELECT_ID)
  .addEventListener("change", async function (event) {
    const value = event.target.value;
    const exercises = filterExercises({
      exercises: CONTEXT.exercises,
      muscleId: value,
      equipmentId: EQUIPMENT_SELECT.value,
    });
    updateExerciseSelectRoot({
      exercises: exercises,
      rootElement: EXERCISES_SELECT_ROOT,
    });
  });

document
  .getElementById(EQUIPMENT_SELECT_ID)
  .addEventListener("change", async function (event) {
    const value = event.target.value;
    const exercises = filterExercises({
      exercises: CONTEXT.exercises,
      muscleId: MUSCLE_SELECT.value,
      equipmentId: value,
    });
    updateExerciseSelectRoot({
      exercises: exercises,
      rootElement: EXERCISES_SELECT_ROOT,
    });
  });
