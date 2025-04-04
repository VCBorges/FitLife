# FitLife

## Description

FitLife is a web application developed to help users manage their workouts and track their physical progress. The platform offers functionalities such as creating workouts, tracking exercises, and managing user profiles.

## Features

- **User Authentication**: User registration, login, and logout.
- **Profile Management**: Updating personal information and preferences.
- **Workout Creation**: Allows users to create and customize their workouts.
- **Exercise Tracking**: Logging and monitoring of completed exercises.
- **Administration**: Administrative interface to manage users and content.

## Technologies Used

### Backend

- **Django**: Web framework used to build the application.
- **Django-Cotton**: Library for creating reusable components in Django templates.
- **PostgreSQL**: Relational database used to store application data.

### Frontend

- **HTMX**: JavaScript library that allows adding advanced interactivity to HTML using only attributes.
- **Alpine.js**: JavaScript framework for adding interactivity to HTML.
- **Bootstrap**: CSS framework for styling components.
- **LESS**: CSS preprocessor to simplify writing styles.

## Project Structure

- **apps/**: Contains the Django apps of the application.
  - **core/**: Core functionalities and utilities.
  - **users/**: User management and authentication.
  - **gym/**: Functionalities related to workouts and exercises.
- **config/**: Django project configurations.
- **templates/**: HTML templates used in the application.
- **static/**: Static files like CSS, JavaScript, and images.
- **tests/**: Automated tests for the application.

## How to Run

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/fitlife.git
    cd fitlife
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    poetry install
    ```

4. Configure the environment variables:
    Create a `.env` file at the root of the project and add the necessary variables, such as `SECRET_KEY` and `DEBUG`.

5. Run the database migrations:
    ```sh
    python manage.py migrate
    ```

6. Start the development server:
    ```sh
    python manage.py runserver
    ```
