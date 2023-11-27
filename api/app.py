from flask import Flask, request, jsonify, g
import sqlite3

app = Flask(__name__)

DATABASE = 'university.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Database Initialization
with app.app_context():
    db = get_db()
    cursor = db.cursor()
    

# API Endpoints
@app.route('/students', methods=['POST'])
def create_student():
    db = get_db()
    cursor = db.cursor()
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']

    cursor.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
    db.commit()

    student_id = cursor.lastrowid
    return jsonify({"message": "Student created successfully", "student_id": student_id})
    

@app.route('/courses', methods=['POST'])
def create_course():
    db = get_db()
    cursor = db.cursor()
    data = request.get_json()
    course_name = data['course_name']
    course_code = data['course_code']
    description = data['description']

    cursor.execute("INSERT INTO courses (course_name, course_code, description) VALUES (?, ?, ?)", (course_name, course_code, description))
    db.commit()

    course_id = cursor.lastrowid
    return jsonify({"message": "Course created successfully", "course_id": course_id})

@app.route('/students/<int:student_id>/courses/<int:course_id>', methods=['POST'])
def enroll_student_in_course(student_id, course_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
    db.commit()
    return jsonify({"message": "Student enrolled in course successfully"})

@app.route('/students/<int:student_id>/courses/<int:course_id>', methods=['DELETE'])
def remove_student_from_course(student_id, course_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM student_courses WHERE student_id = ? AND course_id = ?", (student_id, course_id))
    db.commit()
    return jsonify({"message": "Student removed from course successfully"})


@app.route('/students/<int:student_id>/courses', methods=['GET'])
def get_courses_for_student(student_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT course_id FROM student_courses WHERE student_id = ?", (student_id,))
    course_ids = [row[0] for row in cursor.fetchall()]
    courses = []
    for course_id in course_ids:
        cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
        courses.append(cursor.fetchone())
    return jsonify(courses)

@app.route('/students/<int:student_id>/courses/not-taken', methods=['GET'])
def get_courses_not_taken_by_student(student_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM courses")
    all_course_ids = set(row[0] for row in cursor.fetchall())
    cursor.execute("SELECT course_id FROM student_courses WHERE student_id = ?", (student_id,))
    taken_course_ids = set(row[0] for row in cursor.fetchall())
    not_taken_course_ids = all_course_ids - taken_course_ids
    courses = []
    for course_id in not_taken_course_ids:
        cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
        courses.append(cursor.fetchone())
    return jsonify(courses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)

