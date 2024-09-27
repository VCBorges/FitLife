import { handleFormSubmit } from "../../../core/forms.js";
import { getContext } from "../../../core/utils.js";
import {  } from "../services/gym.js";

const DELETE_WORKOUT_BTN_CLS = ".delete-workout-btn";
const WORKOUT_LIST_ITEM_CLS = ".workout-list-item";

const CONTEXT = getContext()


async function handleSubmitDeleteWorkoutForm(event){
    await handleFormSubmit({ event })

}