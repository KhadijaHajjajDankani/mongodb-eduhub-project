from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime

# Load environment variables
load_dotenv()
uri = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(uri)
db = client["eduhub_db"]

# 1. Add a new user
def add_user(user_data):
    user_data["dateJoined"] = datetime.datetime.utcnow().isoformat()
    result = db.users.insert_one(user_data)
    print(f"✅ User added with _id: {result.inserted_id}")

# 2. Add a new course
def add_course(course_data):
    course_data["createdAt"] = datetime.datetime.utcnow().isoformat()
    course_data["updatedAt"] = course_data["createdAt"]
    result = db.courses.insert_one(course_data)
    print(f"✅ Course added with _id: {result.inserted_id}")

# 3. Enroll a student
def enroll_student(enrollment_data):
    enrollment_data["dateEnrolled"] = datetime.datetime.utcnow().isoformat()
    result = db.enrollments.insert_one(enrollment_data)
    print(f"✅ Enrollment created with _id: {result.inserted_id}")

# 4. Add a lesson
def add_lesson(lesson_data):
    result = db.lessons.insert_one(lesson_data)
    print(f"✅ Lesson added with _id: {result.inserted_id}")





    # -----------------------
# PART 3.2 – READ METHODS
# -----------------------

# 1. Get all students enrolled in a course
def get_students_in_course(course_id):
    enrollments = db.enrollments.find({"courseId": course_id})
    student_ids = [e["studentId"] for e in enrollments]
    students = db.users.find({"userId": {"$in": student_ids}})
    print(f"\n📘 Students in course {course_id}:")
    for s in students:
        print(f"- {s['firstName']} {s['lastName']} ({s['email']})")

# 2. Get course details by title
def get_course_by_title(title):
    course = db.courses.find_one({"title": title})
    if course:
        print(f"\n📘 Course Found: {course['title']} - {course['description']}")
    else:
        print("❌ Course not found.")

# 3. Get user info by email
def get_user_by_email(email):
    user = db.users.find_one({"email": email})
    if user:
        print(f"\n👤 User Found: {user['firstName']} {user['lastName']} ({user['role']})")
    else:
        print("❌ User not found.")

# 4. List all lessons in a course (ordered)
def get_lessons_in_course(course_id):
    lessons = db.lessons.find({"courseId": course_id}).sort("order", 1)
    print(f"\n📘 Lessons in course {course_id}:")
    for l in lessons:
        print(f"- Lesson {l['order']}: {l['title']}")



        # -----------------------
# PART 3.3 – UPDATE METHODS
# -----------------------

# 1. Update course title and/or price
def update_course(course_id, new_title=None, new_price=None):
    updates = {}
    if new_title:
        updates["title"] = new_title
    if new_price:
        updates["price"] = new_price
    updates["updatedAt"] = datetime.datetime.utcnow().isoformat()

    result = db.courses.update_one(
        {"courseId": course_id},
        {"$set": updates}
    )
    print(f"✅ Updated {result.modified_count} course(s).")

# 2. Update lesson content
def update_lesson_content(lesson_id, new_content):
    result = db.lessons.update_one(
        {"lessonId": lesson_id},
        {"$set": {"content": new_content}}
    )
    print(f"✅ Updated content for lesson {lesson_id}.")

# 3. Update user profile (optional)
def update_user_bio(user_id, new_bio):
    result = db.users.update_one(
        {"userId": user_id},
        {"$set": {"profile.bio": new_bio}}
    )
    print(f"✅ Updated bio for user {user_id}.")



    # -----------------------
# PART 3.4 – DELETE METHODS
# -----------------------

# 1. Soft delete a user (mark inactive)
def soft_delete_user(user_id):
    result = db.users.update_one(
        {"userId": user_id},
        {"$set": {"isActive": False}}
    )
    print(f"✅ Soft deleted user {user_id} (marked inactive).")

# 2. Hard delete a course
def hard_delete_course(course_id):
    result = db.courses.delete_one({"courseId": course_id})
    print(f"✅ Hard deleted {result.deleted_count} course(s) with ID {course_id}.")