import { handleRequestSubmit } from "../../core/requests.js";

export class WorkoutsList {
  /**
   * @param {{
   * rootElementSelector: string,
   * }} props
   */
  constructor({ rootElementSelector }) {
    /**@type {HTMLDivElement} */
    this.rootElement = document.querySelector(rootElementSelector);
    /**@type {String} */
    this.endpoint = this.rootElement.getAttribute("data-endpoint");
    this.searchInput = this.rootElement.querySelector(".search-input");
    this.searchInput.addEventListener("input", async () => {
      await this.fetchWorkouts();
    });
  }

  async fetchWorkouts() {
    const workouts = await handleRequestSubmit({
      url: this.endpoint,
      method: "GET",
      data: {
        search: this.searchInput.value,
      },
    });
    
  }
}
