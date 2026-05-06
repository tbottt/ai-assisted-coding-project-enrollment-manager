# Enrollment Structure Analysis

## Database vs Service Responsibilities

### Mixed Responsibilities
- **DB_PATH, SNAPSHOT_PATH, statuses, CURRENT_STUDENT**:
  - **Task**: Mixed (Cross Layer)
  - **State/Data**: Reads global state
  - **Design**: Constants/configuration are used globally, which mixes concerns between database and service layers.

- **enroll_with_key**:
  - **Task**: Mixed (Cross Layer)
  - **State/Data**: Requires passing state
  - **Design**: Combines database operations (SQL) with service logic (enrollment rules).

- **soft_unenroll_student**:
  - **Task**: Mixed (Cross Layer)
  - **State/Data**: Requires passing state
  - **Design**: Combines database updates with service-level decisions.

- **export_database_snapshot**:
  - **Task**: Mixed (Cross Layer)
  - **State/Data**: Self-contained
  - **Design**: Combines database querying with JSON export logic.

- **main runner**:
  - **Task**: Mixed (Cross Layer)
  - **State/Data**: Reads global state
  - **Design**: Combines database setup, service logic, and testing flow.

### Database-Only Responsibilities
- **connect**:
  - **Task**: Single Task
  - **State/Data**: Self-contained
  - **Design**: Cleanly handles database connection setup.

- **create_tables**:
  - **Task**: Single Task
  - **State/Data**: Self-contained
  - **Design**: Cleanly creates database schema.

- **seed_sample_data**:
  - **Task**: Mixed (Same Layer)
  - **State/Data**: Self-contained
  - **Design**: Seeds both courses and enrollments, which could be split for clarity.

- **SQLite SELECT, INSERT, UPDATE**:
  - **Task**: Single Task
  - **State/Data**: Requires passing state
  - **Design**: Clean database operations, but scattered across functions.

### Service-Only Responsibilities
- **AVAILABLE_COURSE_KEYS**:
  - **Task**: Single Task
  - **State/Data**: Self-contained
  - **Design**: Acts as a constant for service logic.

- **get_student_summary**:
  - **Task**: Mixed (Same Layer)
  - **State/Data**: Requires passing state
  - **Design**: Aggregates data for service-level reporting.

- **get_all_enrollment_records**:
  - **Task**: Single Task
  - **State/Data**: Self-contained
  - **Design**: Provides a snapshot of all enrollment data.

### Unclear or Scattered Design
- **get_available_course_keys**:
  - **Task**: Single Task
  - **State/Data**: Self-contained
  - **Design**: Database query, but its purpose is service-level (UI display).

- **get_course_by_key**:
  - **Task**: Single Task
  - **State/Data**: Requires passing state
  - **Design**: Database query, but its purpose is service-level (enrollment validation).

- **get_student_enrollments**:
  - **Task**: Single Task
  - **State/Data**: Requires passing state
  - **Design**: Database query, but its purpose is service-level (dashboard display).

- **get_student_enrollment_history**:
  - **Task**: Single Task
  - **State/Data**: Requires passing state
  - **Design**: Database query, but its purpose is service-level (history reporting).

- **rows_to_dicts**:
  - **Task**: Single Task
  - **State/Data**: Self-contained
  - **Design**: Utility function, but its usage is scattered.

## Single Responsibility Violations
- **enroll_with_key**:
  - Combines database operations (INSERT/UPDATE) with service logic (key validation, reactivation).

- **soft_unenroll_student**:
  - Combines database updates with service-level decisions about "soft" unenrollment.

- **export_database_snapshot**:
  - Combines database querying with JSON export logic.

- **seed_sample_data**:
  - Seeds both courses and enrollments, which could be split for clarity.

- **main runner**:
  - Combines database setup, service logic, and testing flow.

## Global State Usage
- **DB_PATH, SNAPSHOT_PATH, statuses, CURRENT_STUDENT**:
  - Used globally, making the code less modular and harder to test.

## Clean vs Mixed Design Examples
- **Clean DB-Only Work**:
  - `connect`, `create_tables`, `seed_sample_data` (partially), `SQLite SELECT/INSERT/UPDATE`.

- **Mixed or Unclear Design**:
  - `enroll_with_key`, `soft_unenroll_student`, `export_database_snapshot`, `main`.

## Scattered Responsibilities
- Database operations (SQL) are scattered across functions like `get_student_enrollments`, `get_course_by_key`, and `enroll_with_key`.
- Service logic (enrollment rules, summaries) is mixed with database logic in functions like `enroll_with_key` and `soft_unenroll_student`.
- Utility functions like `rows_to_dicts` are used inconsistently across the codebase.