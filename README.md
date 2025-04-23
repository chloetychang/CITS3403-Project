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
`pip install -r requirements.txt`
```

When a dependency has been added, the requirements file should be updated with the command `pip freeze > requirements.txt`.

### Launching the Application
After setting up the virtual environment and installing the dependencies, run the command:

```bash
flask run
```

(For development, so the server does not have to be stopped and reran as we create modifications, run `flask run --debug`)

## Instructions: How to run the tests for the application
