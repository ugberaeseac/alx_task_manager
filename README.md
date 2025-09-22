# ALX Task Manager

## Setup and Run Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd alx_task_manager
    ```
2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Apply migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```
6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`

## Features Implemented

*   User Registration and Authentication
*   Custom User Model with additional fields (email, first name, last name)
*   Task Management (creation, viewing, updating, deletion)
*   Project Management (creation, viewing, updating, deletion)

## Technologies Used

*   Python
*   Django
*   SQLite (default database)
*   HTML/CSS

## Notes on AI Usage

This project was developed with the assistance of an AI coding assistant. The AI was used for:

*   **Code Generation:** Generating boilerplate code, model definitions, forms, and views.
*   **Debugging:** Identifying and suggesting fixes for errors, including migration issues and import errors.
*   **Code Refactoring:** Suggesting improvements to existing code.
*   **Guidance:** Providing instructions and explanations for Django concepts and best practices.
*   **File Management:** Creating and modifying files as needed.