from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Connect to MongoDB
load_dotenv()
uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
db = client["eduhub_db"]

# -----------------------------
# PART 4 – AGGREGATION QUERIES
# -----------------------------

# 4.1 – List all students enrolled in a course with progress & status
def get_enrolled_students(course_id):
    pipeline = [
        {"$match": {"courseId": course_id}},
        {
            "$lookup": {
                "from": "users",
                "localField": "studentId",
                "foreignField": "userId",
                "as": "studentInfo"
            }
        },
        {"$unwind": "$studentInfo"},
        {
            "$project": {
                "_id": 0,
                "studentName": {
                    "$concat": ["$studentInfo.firstName", " ", "$studentInfo.lastName"]
                },
                "email": "$studentInfo.email",
                "progress": 1,
                "status": 1
            }
        }
    ]
    results = db.enrollments.aggregate(pipeline)
    print(f"\n📘 Students in course {course_id}:")
    for r in results:
        print(f"- {r['studentName']} ({r['email']}) – {r['progress']}, {r['status']}")

# 4.2 – Count how many students each instructor teaches
def count_students_per_instructor():
    pipeline = [
        {
            "$lookup": {
                "from": "courses",
                "localField": "courseId",
                "foreignField": "courseId",
                "as": "courseInfo"
            }
        },
        {"$unwind": "$courseInfo"},
        {
            "$group": {
                "_id": "$courseInfo.instructorId",
                "studentsTaught": {"$sum": 1}
            }
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "_id",
                "foreignField": "userId",
                "as": "instructor"
            }
        },
        {"$unwind": "$instructor"},
        {
            "$project": {
                "instructor": {
                    "$concat": ["$instructor.firstName", " ", "$instructor.lastName"]
                },
                "studentsTaught": 1
            }
        }
    ]
    results = db.enrollments.aggregate(pipeline)
    print("\n🧑‍🏫 Students per instructor:")
    for r in results:
        print(f"- {r['instructor']}: {r['studentsTaught']} students")

# 4.3 – Average grade per assignment
def average_grade_per_assignment():
    pipeline = [
        {
            "$group": {
                "_id": "$assignmentId",
                "averageGrade": {"$avg": "$grade"}
            }
        },
        {
            "$lookup": {
                "from": "assignments",
                "localField": "_id",
                "foreignField": "assignmentId",
                "as": "assignment"
            }
        },
        {"$unwind": "$assignment"},
        {
            "$project": {
                "assignment": "$assignment.title",
                "averageGrade": {"$round": ["$averageGrade", 2]}
            }
        }
    ]
    results = db.submissions.aggregate(pipeline)
    print("\n📈 Average grades by assignment:")
    for r in results:
        print(f"- {r['assignment']}: {r['averageGrade']}%")

# 4.4 – Enrollment stats per course
def enrollment_stats():
    pipeline = [
        {
            "$group": {
                "_id": "$courseId",
                "numStudents": {"$sum": 1}
            }
        },
        {
            "$lookup": {
                "from": "courses",
                "localField": "_id",
                "foreignField": "courseId",
                "as": "course"
            }
        },
        {"$unwind": "$course"},
        {
            "$project": {
                "course": "$course.title",
                "enrollments": "$numStudents"
            }
        }
    ]
    results = db.enrollments.aggregate(pipeline)
    print("\n📊 Enrollments per course:")
    for r in results:
        print(f"- {r['course']}: {r['enrollments']} students")