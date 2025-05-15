# CITS3403-Project
CITS3403 - Agile Web Development Project

## 📝 Description

The Sleep Tracker is a web app that allows users to log sleep and wake times, rate their sleep quality, and view weekly trends through interactive graphs. It is designed with a user-friendly interface and aims to help individuals improve sleep habits by recognizing patterns and behaviors.


## Group Members: UWA ID, Name and Github Username
| Student ID | Student Name     | GitHub Username |
|------------|------------------|-----------------|
| 23399936   | Liam O'Brien     | limeken         |
| 23722854   | Chloe Chang      | chloetychang    |
| 23887876   | Gargi Garg       | Gg1803          |
| 24115877   | Kimberley Lee    | kimberley25     |


## Instructions: How to launch the application

### Virtual Environment
Set up the virtual environment using the following commands:

```bash
python -m venv venv
source venv/bin/activate    # In windows, use `venv\Scripts\activate`
```

### Project Dependencies
Install dependencies using the command:
```bash
pip install -r requirements.txt
```

When a dependency has been added, the requirements file should be updated with the command `pip freeze > requirements.txt`.

### Before Launching the Application
Before running the application, ensure you set a secret key for Flask. You can do this by exporting an environment variable. Run the following command in your terminal:
```bash
export SECRET_KEY='your_secret_key_here'
```
Replace `'your_secret_key_here'` with a strong, random string.

### Launching the Application
After setting up the virtual environment, installing the dependencies, and setting your unique secret key run the command:

```bash
flask run
```

(For development, so the server does not have to be stopped and reran as we create modifications, run `flask run --debug`)

### Initialise the Database 
To initialise the database, run: 
```bash
flask db upgrade
```
This will create the database and apply both existing migrations (initial and second).

## 🧪 Instructions: How to Run Tests
There are no automated test scripts included at this stage.
You can manually test the application by:

##🧰 Tech Stack

Backend: Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF

Frontend: Tailwind CSS, Plotly.js, Jinja2 templates

Database: SQLite (via SQLAlchemy)

Utilities: Flask-Migrate, JavaScript (for flash messages and popups)

##📁 Project Structure

CITS3403-Project/
├── app/
│   ├── __init__.py       # App config and factory
│   ├── routes.py         # Routes and logic
│   ├── models.py         # DB models (User, Entry)
│   ├── forms.py          # WTForms
│   ├── plot.py           # Graph generation
│   ├── templates/        # HTML pages
│   └── static/           # JS, icons
├── migrations/           # DB migration scripts
├── app.db                # SQLite DB (auto-generated)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation


## 🧪 How to Use the Application

Once the app is running locally:

1. **Register a User** – Go to the Sign-Up page and create an account by entering your details.
2. **Log In** – Access the login page and sign in using your registered email and password.
3. **Add Sleep Records** – On the Sleep or Records page, input your sleep and wake times, and optionally rate your mood.
4. **View Results** – Navigate to the Results page to see your weekly sleep analysis as an interactive graph.
5. **Logout** – Click the logout icon to securely end your session.

## 🚀 Getting Started

### Login
You can use the following test account to log in:

- **Username**: `admin`  
- **Email**: `admin@example.com`  
- **Password**: `admin123`


### Registration
New users can sign up by providing the required information. Once registered, you may log in using your new credentials.

### 📝 Sign Up

New users can create an account by providing basic details like name, age, and email, then log in to begin tracking their sleep.


## 🧭 App Navigation

- **Sleep Page**: Upload your sleep and wake times, rate your mood, and manage entries.
- **Records Page**: View a calendar with all your logged entries; edit or add new ones.
- **Results Page**: Visualize your weekly sleep trends using an interactive Plotly graph.
- **Logout**: Securely end your session anytime using the logout option.


## 🧪 Instructions: How to Run Tests

This project includes **automated unit tests** and **Selenium WebDriver system tests**.

### 🔹 Unit Tests

The following files implement unit tests using Python’s built-in `unittest` framework:

- `test_login.py`
- `test_signup.py`
- `test_routes.py`
- `test_backend_auth.py`

Each test file uses a memory-based test database (`sqlite:///:memory:`), and CSRF protection is disabled for isolated test environments.

To run all unit tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```
##🔹 Selenium System Tests

Selenium tests are located in:

base_selenium.py

These simulate user actions in a browser using headless Chrome and test the full application stack, including routing, layout rendering, and public-facing views.

To run Selenium tests, install the following:

```bash
python tests/base_selenium.py
```
