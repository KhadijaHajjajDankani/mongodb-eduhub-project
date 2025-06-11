from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
db = client["eduhub_db"]

# -------------------------------
# PART 6 – VALIDATION & HANDLING
# -------------------------------

# 1. Add user with basic validation
def safe_add_user(user_data):
    try:
        # Required fields check
        required_fields = ["userId", "email", "firstName", "lastName", "role"]
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")

        # Email uniqueness check
        if db.users.find_one({"email": user_data["email"]}):
            raise ValueError("Email already exists.")

        # Insert
        db.users.insert_one(user_data)
        print("✅ User added successfully.")

    except ValueError as ve:
        print(f"❌ Validation Error: {ve}")
    except errors.DuplicateKeyError:
        print("❌ Duplicate Key Error.")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

# 2. Add course with validation
def safe_add_course(course_data):
    try:
        if "courseId" not in course_data or "title" not in course_data:
            raise ValueError("Missing courseId or title")

        db.courses.insert_one(course_data)
        print("✅ Course added successfully.")

    except ValueError as ve:
        print(f"❌ Validation Error: {ve}")
    except Exception as e:
        print(f"❌ Error adding course: {e}")