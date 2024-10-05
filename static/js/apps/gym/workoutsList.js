import { handleRequestSubmit } from "../../core/requests.js";

export const DELETE_WORKOUT_MODAL_ID = 'delete-workout-modal-id';
export const DELETE_WORKOUT_BTN_ID = 'delete-workout-btn-id';


/**
 * @param {{
 * button: HTMLButtonElement,
 * }} props
 */
export function handleClickDeleteWorkoutModalBtn({ button }){
  const modal = document.getElementById(DELETE_WORKOUT_MODAL_ID);
  const deleteWorkoutBtn = modal.getElementById(DELETE_WORKOUT_BTN_ID)
  deleteWorkoutBtn.setAttribute('hx-delete', button.dataset.deleteUrl);
}