# MongoDB EduHub Project – AltSchool Africa

This project is a MongoDB-powered backend system for an educational platform called EduHub. It is part of the Tinyuka Data Engineering second-semester exam at AltSchool Africa.

## ✅ Features Implemented

### 1. Database & Sample Data
- Designed collections: users, courses, enrollments, lessons, assignments, submissions
- Inserted 20 users, 8 courses, 15 enrollments, 25 lessons, 10 assignments, 12 submissions

### 2. CRUD Operations
- Create, read, update, and delete logic implemented in crud_operations.py
- Sample usage in test_crud.py

### 3. Aggregation Queries
- Advanced queries for analytics (e.g., students per course, instructor performance)
- Implemented in aggregation_queries.py

### 4. Indexing & Performance
- Cleaned duplicate data
- Created unique indexes and performance indexes in indexing.py

### 5. Validation & Error Handling
- Handled duplicate emails and missing fields in validation.py

---

## 🛠 How to Run

1. Install dependencies:
   ```bash
   pip install pymongo python-dotenv