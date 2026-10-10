
# Student Management REST API

A RESTful API built with Python, Flask, and SQLite.

## Features
- Create student records
- Get all students
- Get a student by ID
- Update student details
- Delete student records
- Input validation and JSON error handling
- SQLite database integration
- Automated tests

## Technologies
- Python
- Flask
- SQLite
- Postman
- Git and GitHub

## Installation

Create a virtual environment:

python -m venv venv

Activate on Windows PowerShell:

.\venv\Scripts\Activate.ps1

Install dependencies:

python -m pip install -r requirements.txt

Run the API:

python app.py

Base URL: http://127.0.0.1:5000

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/students | Create a student |
| GET | /api/students | Get all students |
| GET | /api/students/{id} | Get one student |
| PUT | /api/students/{id} | Update a student |
| DELETE | /api/students/{id} | Delete a student |

## Documentation

See docs/API_DOCUMENTATION.md.

## Testing

Run:

python -m pytest -q

## Database

SQLite creates students.db automatically.
The database is excluded from Git because each
user generates their own local database.

## Author

Kranti Hajare