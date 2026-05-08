import streamlit as st
from enrollment_starter import (
    connect,
    STATUS_ENROLLED,
    STATUS_UNENROLLED,
    get_all_enrollment_records,
    get_student_enrollment_history,
    seed_sample_data,
)

# Simulated student
CURRENT_STUDENT = {
    "user_id": "u100",
    "name": "Maya Patel",
    "email": "maya.patel@example.edu",
}

# Initialize the database and seed data
seed_sample_data()

# Helper function to fetch enrolled classes for the current student
def get_enrolled_classes(user_id):
    with connect() as connection:
        cursor = connection.execute(
            """
            SELECT c.course_name, c.instructor, e.status
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            WHERE e.user_id = ? AND e.status = ?
            """,
            (user_id, STATUS_ENROLLED),
        )
        return cursor.fetchall()

# Helper function to enroll a student in a course
def enroll_student(user_id, enrollment_key):
    with connect() as connection:
        # Check if the enrollment key is valid
        cursor = connection.execute(
            """
            SELECT course_id FROM courses WHERE enrollment_key = ?
            """,
            (enrollment_key,),
        )
        course = cursor.fetchone()
        if not course:
            return False, "Invalid enrollment key."

        course_id = course[0]

        # Enroll the student in the course
        connection.execute(
            """
            INSERT OR IGNORE INTO enrollments (user_id, course_id, status)
            VALUES (?, ?, ?)
            """,
            (user_id, course_id, STATUS_ENROLLED),
        )
        return True, f"Successfully enrolled in course {course_id}."

# Helper function to unenroll a student from a course
def unenroll_student(user_id, course_id):
    with connect() as connection:
        connection.execute(
            """
            UPDATE enrollments
            SET status = ?
            WHERE user_id = ? AND course_id = ?
            """,
            (STATUS_UNENROLLED, user_id, course_id),
        )
        return f"You have unenrolled from course {course_id}."

# Streamlit app
st.title("Student Enrollment Dashboard")

# Display current student info
st.sidebar.header("Student Info")
st.sidebar.write(f"Name: {CURRENT_STUDENT['name']}")
st.sidebar.write(f"Email: {CURRENT_STUDENT['email']}")

# Fetch and display enrolled classes
st.header("My Enrolled Classes")
enrolled_classes = get_enrolled_classes(CURRENT_STUDENT["user_id"])
if enrolled_classes:
    for course_name, instructor, status in enrolled_classes:
        with st.expander(f"{course_name} (Instructor: {instructor})"):
            col1, col2 = st.columns(2)
            if col1.button("Unenroll", key=f"unenroll_{course_name}"):
                unenroll_message = unenroll_student(CURRENT_STUDENT["user_id"], course_name)
                st.session_state["feedback_message"] = unenroll_message
                st.experimental_rerun()
else:
    st.write("You are not enrolled in any classes.")

st.divider()

# Enrollment key input
st.header("Enroll in a New Class")
enrollment_key = st.text_input("Enter Enrollment Key")
if st.button("Submit Enrollment Key"):
    success, message = enroll_student(CURRENT_STUDENT["user_id"], enrollment_key)
    if success:
        st.success(message)
        st.experimental_rerun()
    else:
        st.error(message)

# Feedback message display
if "feedback_message" in st.session_state and st.session_state["feedback_message"]:
    st.info(st.session_state["feedback_message"])
    st.session_state["feedback_message"] = None