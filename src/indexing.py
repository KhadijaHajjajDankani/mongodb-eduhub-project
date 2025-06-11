from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load the environment variable
load_dotenv()
uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
db = client["eduhub_db"]

# -------------------------------
# PART 5 – INDEXING & CLEANUP
# -------------------------------

# ✅ STEP 1: Remove duplicate emails
def remove_duplicate_emails():
    print("\n🧹 Checking for duplicate emails...")

    # Group users by email
    pipeline = [
        {
            "$group": {
                "_id": "$email",
                "ids": {"$push": "$_id"},
                "count": {"$sum": 1}
            }
        },
        {"$match": {"count": {"$gt": 1}}}
    ]

    duplicates = list(db.users.aggregate(pipeline))
    total_removed = 0

    for entry in duplicates:
        ids = entry["ids"]
        ids_to_delete = ids[1:]  # Keep 1, delete the rest
        result = db.users.delete_many({"_id": {"$in": ids_to_delete}})
        total_removed += result.deleted_count

    if total_removed > 0:
        print(f"🧹 Removed {total_removed} duplicate user(s).")
    else:
        print("✅ No duplicates found.")

# ✅ STEP 2: Create unique indexes
def create_indexes():
    print("\n📌 Creating indexes...")

    # Drop old email index if it exists
    try:
        db.users.drop_index("email_1")
        print("⚠️  Old 'email' index dropped.")
    except Exception:
        print("ℹ️  No previous 'email' index found.")

    # Now create a clean unique index on email
    db.users.create_index("email", unique=True)
    print("✅ Unique index on email created.")

    # Other recommended indexes
    db.courses.create_index("courseId")
    db.enrollments.create_index("courseId")
    db.enrollments.create_index("studentId")
    db.assignments.create_index("assignmentId")
    db.submissions.create_index("assignmentId")
    print("✅ All other indexes created.")

# ✅ STEP 3: View all current indexes
def list_indexes():
    print("\n📄 Current indexes in each collection:")
    for name in ["users", "courses", "enrollments", "assignments", "submissions"]:
        print(f"\n📁 {name.upper()} indexes:")
        for index in db[name].list_indexes():
            print(index)