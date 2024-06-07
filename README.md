# SecureNotes

SecureNotes is a web application developed using Django, JavaScript, HTML, and CSS, providing users with a **secure** platform to manage their notes.

## Features

1. **Technology Stack**: SecureNotes is built using Django, JavaScript, HTML, and CSS.

2. **User Authentication**: Users can register for an account, log in securely, and manage their sessions.

3. **Note Management**: Users can create, edit, and delete notes.

4. **Encryption**: Before saving notes to the database, Fernet symmetric encryption is used to encrypt the content of the notes. The notes are decrypted when displayed to ensure security.

## How to Run

To run SecureNotes locally:

1. Clone the repository:

    ```bash
    git clone https://github.com/Zizo0004/SecureNotes.git
    ```

2. Navigate to the project directory:

    ```bash
    cd SecureNotes
    ```

3. Run the Django development server:

    ```bash
    python manage.py runserver
    ```

4. Open a web browser and navigate to [http://127.0.0.1:8000/signup](http://127.0.0.1:8000/signup) to register for a new account.

5. If already registered and logged in, go to [http://127.0.0.1:8000/home](http://127.0.0.1:8000/home) to access the home page.

## Database Access

To view the database:

1. Create a superuser account:

    ```bash
    python manage.py createsuperuser
    ```

2. Log in to the Django admin interface:

    [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

## Note

Ensure that Django and any required dependencies are installed before running the application.
To utilize **Crispy Forms** for the form layout (login and register), ensure you have them installed in your project.

### Installing Crispy Forms

You can install Crispy Forms using pip:

```bash
pip install django-crispy-forms

