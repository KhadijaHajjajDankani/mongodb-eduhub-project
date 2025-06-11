from crud_operations import add_user

add_user({
    "userId": "U021",
    "email": "student21@example.com",
    "firstName": "Khadija",
    "lastName": "Dankani",
    "role": "student",
    "profile": {
        "bio": "Student of MongoDB",
        "avatar": "",
        "skills": ["MongoDB", "Python"]
    },
    "isActive": True
})



from crud_operations import get_user_by_email, get_course_by_title, get_students_in_course, get_lessons_in_course

get_user_by_email("student21@example.com")
get_course_by_title("Course 1")
get_students_in_course("C001")
get_lessons_in_course("C001")



from crud_operations import update_course, update_lesson_content, update_user_bio

update_course("C001", new_title="Updated Course 1", new_price=99)
update_lesson_content("L001", "Updated content for lesson 1.")
update_user_bio("U021", "Khadija is now a MongoDB queen 👑")



from crud_operations import soft_delete_user, hard_delete_course

soft_delete_user("U021")
hard_delete_course("C008")