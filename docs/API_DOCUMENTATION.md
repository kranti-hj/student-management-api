
# Student Management API Documentation

## Base URL
http://127.0.0.1:5000

## Student Data Model

| Field | Type | Description |
|---|---|---|
| id | Integer | Auto-generated ID |
| name | String | Student name |
| email | String | Unique email |
| course | String | Student course |
| age | Integer | Age from 1 to 120 |

## 1. Create Student
POST /api/students

Request body:
```json
{
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "course": "CSE Data Science",
  "age": 21
}
```

Success: 201 Created

## 2. Get All Students
GET /api/students

Success: 200 OK

## 3. Get Student by ID
GET /api/students/{student_id}

Success: 200 OK
Error: 404 Not Found

## 4. Update Student
PUT /api/students/{student_id}

Send all four fields: name, email, course, age.

Success: 200 OK
Errors: 400, 404, 409

## 5. Delete Student
DELETE /api/students/{student_id}

Success: 200 OK
Error: 404 Not Found

## Error Codes

| Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Student created |
| 400 | Invalid input |
| 404 | Record or route not found |
| 405 | Method not allowed |
| 409 | Duplicate email |
| 500 | Internal server error |

## Database
SQLite database: students.db