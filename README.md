# CITS3403-Project

CITS3403 - Agile Web Development Project

## 📝 Description

The Sleep Tracker is a comprehensive web application designed to help users monitor and improve their sleep patterns. It offers:

### Key Features

- **Sleep Logging**: Record daily sleep and wake times with mood ratings
- **Data Visualization**: View sleep patterns through interactive graphs and charts
- **Calendar View**: Track sleep records with color-coded indicators
- **Social Features**: Connect with friends and share sleep data with each other

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

### Initialise the Database

To initialise the database, run:

```bash
flask db upgrade
```

This will create the database and apply all existing migrations.

### Launching the Application

After setting up the virtual environment, installing the dependencies, and setting your unique secret key run the command:

```bash
flask run
```

(For development, so the server does not have to be stopped and reran as we create modifications, run `flask run --debug`)

## 🧰 Tech Stack

Backend: Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF

Frontend: Tailwind CSS, Plotly.js, Jinja2 templates

Database: SQLite (via SQLAlchemy)

Utilities: Flask-Migrate, JavaScript (for flash messages and popups)

## How to Use the Application

## 🚀 Getting Started

#### 1. **Sign Up (New Users)**

- Navigate to the **Sign-Up** page.
- Fill up the Sign Up form and log in with your new account.

#### 2. **Log In**

- Navigate to the **Login** page.
- Enter using your registered email and password to start using the application.

Test Account:

```bash
Email: <admin@example.com>
Password: admin123
```

### 🌙 Core Features

#### Upload Sleep Data

1. Navigate to the **Sleep** page.
2. Click **Upload Sleep Data** and fill up all the details required.
3. Click **Save Entry** to log your data.

#### View Sleep Records

1. Navigate to the **Records** page to view your sleep entries in a calendar format.
2. Each date is color-coded based on your sleep duration:

   - 🟩 **Green** – 7+ hours
   - 🟨 **Yellow** – 5 - 7 hours
   - 🟥 **Red** – < 5 hours
   - ⬜ **Grey** – No sleep data recorded

3. Click any date to:
   - View detailed sleep data
   - Add a new entry
   - Delete an existing record

#### Analyse Results

1. Navigate the **Results** page.
2. Interact with insightful graphs:
   - Weekly sleep patterns
   - Mood correlations
   - REM cycle pattern

### Share Sleep Data

1. Navigate to the **Share** page.
2. Search for other exisiting users and send a **friend request** to connect.
3. Once accepted, your friend will appear under **Your Friends**.
4. You can then:
   - Click **Show Sleep Data** to view their shared entries.
   - Click **Unfriend** to remove the connection.

#### Notes

- Only **mutual connections** can view each other’s sleep data.
- Pending requests will appear under **Pending Friend Requests**.

### 💡 Tips for Best Use

- Record entries **daily** for accurate tracking.
- Include **mood ratings** to help identify how sleep affects emotional well-being.
- Regularly review **weekly trends** to improve your sleep habits.

## Instructions: How to Run Tests

This project includes **automated unit tests** and **Selenium WebDriver system tests**.

### 🔹 Unit Tests

The following files implement unit tests using Python’s built-in `unittest` framework:

- `test_authentication.py`
- `test_backend_auth.py`
- `test_login.py`
- `test_signup.py`
- `test_upload.py`

Each test file uses a memory-based test database (`sqlite:///:memory:`), and CSRF protection is disabled for isolated test environments.

To run all unit tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## 🔹 Selenium System Tests

Selenium tests are located in:

- `tests/systemTest.py`

These simulate user actions in a browser using headless Chrome and test the full application stack, including routing, layout rendering, and public-facing views.

To run Selenium tests, run the following command:

```bash
python -m tests.systemTest
```
