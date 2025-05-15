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

## Instructions: How to Launch the Application

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

## 🧰 Tech Stack

Backend: Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF

Frontend: Tailwind CSS, Plotly.js, Jinja2 templates

Database: SQLite (via SQLAlchemy)

Utilities: Flask-Migrate, JavaScript (for flash messages and popups)

## How to Use the Application

## 🚀 Getting Started

#### 1. __Sign Up (New Users)__

- Navigate to the __Sign-Up__ page.
- Fill in the form.
- Click __SignUp__ to begin using the app.

#### 2. __Log In__

- Navigate to the __Login__ page.
- Enter using your registered email and password.
- Click __Log In__ to begin using the app.

Example account:
Email: <admin@example.com>
Password: admin123

### 🌙 Core Features

#### Upload Sleep Data

1. Navigate to the __Sleep__ page.
2. Click __Upload Sleep Data__.
3. Fill in the following details:
   - __Sleep Date & Time__
   - __Wake Date & Time__
   - __Mood Rating__
4. Click __Save Entry__ to log your data.

#### View Sleep Records

1. Navigate to the __Records__ page.
2. Browse your sleep entries in a __calendar format__.
3. Each date is __color-coded__ based on your sleep duration:

   - 🟩 __Green__ – Slept __7 hours or more__
   - 🟨 __Yellow__ – Slept between __5 and 7 hours__
   - 🟥 __Red__ – Slept __less than 5 hours__
   - ⬜ __Grey__ – __No sleep data__ recorded for that date.

4. Click on a date to:
   - View detailed sleep data.
   - Add a new entry.
   - Delete an existing record.

#### Analyse Results

1. Navigate the __Results__ page.
2. Interact with insightful graphs:
   - Weekly __sleep patterns__
   - Sleep __duration and consistency trends__
   - __Mood correlations__
   - REM cycle pattern

### 💡 Tips for Best Use

- Record entries __daily__ for accurate tracking.
- Include __mood ratings__ to help identify how sleep affects emotional well-being.
- Regularly review __weekly trends__ to improve your sleep habits.
- Use the __calendar view__ to detect irregularities in your sleep schedule.

## Instructions: How to Run Tests

This project includes __automated unit tests__ and __Selenium WebDriver system tests__.

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

## 🔹 Selenium System Tests

Selenium tests are located in:

base_selenium.py

These simulate user actions in a browser using headless Chrome and test the full application stack, including routing, layout rendering, and public-facing views.

To run Selenium tests, install the following:

```bash
python tests/base_selenium.py
```
