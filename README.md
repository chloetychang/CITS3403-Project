# CITS3403-Project
CITS3403 - Agile Web Development Project

## Description: Purpose of the Application, explaining its Design and Use


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
export FLASK_APP_SECRET_KEY='your_secret_key_here'
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

## Instructions: How to run the tests for the application

## 🚀 Getting Started

### Login
You can use the following test account to log in:

- **Username**: `admin`  
- **Email**: `admin@example.com`  
- **Password**: `admin123`

### Registration
New users can sign up by providing the required information. Once registered, you may log in using your new credentials.