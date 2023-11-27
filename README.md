# University Courses API

This is a simple RESTful API for managing students and courses at a university. It allows you to create students and courses, enroll students in courses, and view which courses a student has taken or not taken.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Docker Compose

### Installing

1. Clone the repository to your local machine.
2. Navigate to the project directory.

```bash
cd path/to/project
```

3. Build and run the Docker containers.

```bash
docker-compose up --build
```

The API server should now be running at `http://localhost:5000`.

## API Endpoints

- `POST /students`: Create a new student.
- `POST /courses`: Create a new course.
- `POST /students/<student_id>/courses/<course_id>`: Enroll a student in a course.
- `DELETE /students/<student_id>/courses/<course_id>`: Remove a student from a course.
- `GET /students/<student_id>/courses`: Get the courses a student has taken.
- `GET /students/<student_id>/courses/not-taken`: Get the courses a student has not taken.

## Built With

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [SQLite](https://www.sqlite.org/index.html) - Database

## Authors

- Varunkumar Inbaraj

