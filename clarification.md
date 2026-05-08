# Streamlit UI Plan for Class Enrollment Management (Updated)

## App Structure and Routing Logic

### App Overview
- The app consists of two pages:
  1. **Dashboard**: Displays the student's enrolled classes and allows enrollment via an enrollment key.
  2. **Class Detail**: Displays detailed information about a selected class and allows soft-unenrollment.

- **Routing**:
  - Use `st.session_state.current_page` to track the current page (`"dashboard"` or `"class_detail"`).
  - Use `st.session_state.selected_class_id` to track the class selected by the student for the detail page.
  - Navigation between pages is handled by updating `st.session_state.current_page`.

- **Session State Variables**:
  - `current_page`: Tracks the current page (`"dashboard"` or `"class_detail"`).
  - `selected_class_id`: Tracks the ID of the class selected for the detail page.
  - `student_role`: Verifies the student's role (e.g., `"student"`).
  - `feedback_message`: Stores success, warning, or error messages to display to the user.

---

## Updates Based on Refinement Questions

### 1. Identifying the Current Student
- The simulated student will be **hardcoded** for simplicity (e.g., `"Alice Johnson"` with `student_id="STU001"`).
- This ensures the app can focus on UI functionality without requiring external configuration or authentication systems.
- The hardcoded student data will be defined at the top of the app script and passed to the service layer as needed.

---

### 2. Class Actions (Go to Class and Unenroll Buttons)
- **Placement**:
  - The "Go to Class" and "Unenroll" buttons will be placed **in an expandable section below each class** in the enrolled classes table.
  - This keeps the main dashboard clean and avoids cluttering the table with too many buttons.
  - Each expandable section will include:
    - A "Go to Class" button to navigate to the class detail page.
    - An "Unenroll" button to allow soft-unenrollment.

---

### 3. Feedback Message Lifecycle
- **When to Clear**:
  - `feedback_message` will clear **after it is displayed** to ensure the user sees the most recent feedback.
  - This will be done automatically after the message is shown on the current page.
- **Persistence**:
  - `feedback_message` will **not persist** if the user navigates back to the dashboard. Instead, it will reset to `None` on page navigation to avoid displaying outdated messages.

---

### 4. Enrollment Key Textbox
- **Auto-Clear**:
  - The enrollment key textbox will **auto-clear after successful enrollment** to improve the user experience and prevent confusion.
- **Manual Clear**:
  - If the enrollment key is invalid, the user will need to manually clear or edit the textbox to try again.

---

## Page 1: Student Dashboard

### Layout and Elements
1. **App Heading**:
   - Use `st.title("My Classes")` to display the app heading.

2. **Enrolled Classes Table**:
   - Use `st.dataframe()` to display a table of enrolled classes with the following columns:
     - Class Name
     - Instructor
     - Semester

3. **Class Actions**:
   - For each enrolled class, add an expandable section below the class row with:
     - A `st.button("Go to Class")` to navigate to the class detail page.
     - A `st.button("Unenroll")` to allow soft-unenrollment.

4. **Horizontal Divider**:
   - Use `st.divider()` to separate the table from the enrollment key input section.

5. **Enrollment Key Input**:
   - Use `st.text_input("Enter Enrollment Key")` to allow the student to input an enrollment key.
   - Add a `st.button("Submit Key")` to submit the key.

6. **Feedback Messages**:
   - Use `st.success()`, `st.warning()`, or `st.error()` to display messages stored in `st.session_state.feedback_message`.
   - Automatically clear `feedback_message` after it is displayed.

---

## Page 2: Selected Class Page

### Layout and Elements
1. **Class Heading**:
   - Use `st.title()` to display the name of the selected class.

2. **Class Information**:
   - Use `st.metric()` or `st.caption()` to display key class details:
     - Instructor
     - Semester
     - Class ID

3. **Horizontal Divider**:
   - Use `st.divider()` to separate the class information from the actions.

4. **Navigation Button**:
   - Add a `st.button("Back to Dashboard")` to return to the dashboard.

5. **Unenrollment Button**:
   - Add a `st.button("Unenroll from This Class")` to allow soft-unenrollment.

---

## Service Layer Method Calls

### Enrollment Key Validation
- When the student enters a key and clicks "Submit Key":
  1. Call `StudentService.validate_enrollment_key()` to validate the key.
  2. If valid:
     - Call `StudentService.enroll_student()` to enroll the student in the class.
     - Add the class to the dashboard.
     - Clear the enrollment key textbox.
     - Refresh the page.
     - Show `st.success("Successfully enrolled!")`.
  3. If invalid:
     - Show `st.error("Invalid enrollment key. Please try again.")`.

### Soft-Unenrollment
- When the student clicks "Unenroll" (on either page):
  1. Call `StudentService.unenroll_student()` to mark the class as unenrolled.
  2. Store a message in `st.session_state.feedback_message` (e.g., `"You have unenrolled from [Class Name]"`).
  3. Refresh the enrolled classes list on the dashboard.
  4. If on the class detail page, navigate back to the dashboard.

### Role Check
- At app startup:
  1. Verify the student's role using the backend (e.g., `student_role == "student"`).
  2. If the role check fails:
     - Show an error message (e.g., `st.error("Access denied. You do not have permission to view this app.")`).
     - Prevent further access to the app.

---

## Error Handling and Feedback Message Flow

1. **Feedback Messages**:
   - Use `st.session_state.feedback_message` to store success, warning, or error messages.
   - Display the message on the appropriate page using `st.success()`, `st.warning()`, or `st.error()`.
   - Automatically clear the message after it is displayed.

2. **Error Scenarios**:
   - Invalid enrollment key: Show `st.error("Invalid enrollment key. Please try again.")`.
   - Role verification failure: Show `st.error("Access denied. You do not have permission to view this app.")`.

---

## Code Outline (Pseudocode)

```python
import streamlit as st

# Initialize session state variables
if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"
if "selected_class_id" not in st.session_state:
    st.session_state.selected_class_id = None
if "feedback_message" not in st.session_state:
    st.session_state.feedback_message = None

# Routing logic
if st.session_state.current_page == "dashboard":
    # Page 1: Dashboard
    # Display enrolled classes, enrollment key input, and class actions
    pass
elif st.session_state.current_page == "class_detail":
    # Page 2: Class Detail
    # Display selected class details and actions
    pass