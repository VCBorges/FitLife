import { handleFormSubmit } from "../../../core/forms.js";
import { getContext } from "../../../core/utils.js";
import { WorkoutsList } from "../workoutsList.js";

const DELETE_WORKOUT_BTN_CLS = ".delete-workout-btn";
const WORKOUT_LIST_ITEM_CLS = ".list-item";
const SELECTORS = {
  TEMPLATES: {
    WORKOUT_LIST_ITEM_ID: "workout-list-item-template-id",
    WORKOUT_EXERCISE_ITEM_ID: "workout-exercise-item-template-id",
  },
};

const CONTEXT = getContext();

/**
 * @param {{
 * template: HTMLTemplateElement,
 * workout: Object,
 * }} props 
 * @returns {HTMLDivElement}
 */
function WorkoutListItem({
  template,
}){
  const component = /** @type {DocumentFragment} */ (
    template.content.cloneNode(true)
  );
  const workoutListItem = component.querySelector(WORKOUT_LIST_ITEM_CLS);
  workoutListItem.dataset.workoutId = workout.id;
  
  const title = workoutListItem.querySelector(".title");
  
}


const workoutList = new WorkoutsList({
  rootElementSelector: ".workouts-list",
});
// async function handleSubmitDeleteWorkoutForm(event){
//     await handleFormSubmit({ event })

// }
