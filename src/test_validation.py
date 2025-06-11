from validation import safe_add_user, safe_add_course

# Test missing field
safe_add_user({
    "userId": "U999",
    "email": "incomplete@example.com",
    "firstName": "MissingLastName",
    "role": "student"
})

# Test duplicate email
safe_add_user({
    "userId": "U888",
    "email": "student21@example.com",  # already exists
    "firstName": "Copy",
    "lastName": "Paste",
    "role": "student"
})

# Test valid course
safe_add_course({
    "courseId": "C999",
    "title": "Crash Course in Validation"
})