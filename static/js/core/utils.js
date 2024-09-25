const HIDDEN_ELEMENT_CLS = "d-none";

/**
 * @param {HTMLElement} element
 * @returns {void}
 */
export function toggleElementVisibility(element) {
  element.classList.toggle(HIDDEN_ELEMENT_CLS);
}

/**
 * @param {HTMLElement} element
 */
export function hideElement(element) {
  element.classList.add(HIDDEN_ELEMENT_CLS);
}

/**
 * @param {HTMLElement} element
 */
export function showElement(element) {
  element.classList.remove(HIDDEN_ELEMENT_CLS);
}

/**
 * @param {String} elementID
 * @returns {Object}
 */
export function getContext(elementID = "context-id") {
  JSON.parse(document.getElementById(elementID).textContent);
}
