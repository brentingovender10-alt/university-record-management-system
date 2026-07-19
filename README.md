# University Record Management System

Group B Database Connection Assignment project for a university record management system.

## Project overview

This repository contains the Group B end-of-module Database Connection Assignment. The project designs and implements a university record management system using a relational database, dummy data, a Python Streamlit interface, query functionality, testing evidence, meeting minutes, a written report and a short demonstration video.

The system allows users to view university records relating to students, lecturers, non-academic staff, courses, departments, programmes and research projects. It also includes a Query Builder page that executes predefined SQL queries through Python and displays the results in the web interface.

## Group roles

| Role | Name | Main responsibilities |
|---|---|---|
| Project Manager | Brentin Govender | GitHub coordination, progress tracking, report quality control, meeting minutes and final submission checklist |
| Database Designer / Engineer | Dooshina Oolun | ERD, normalisation, database schema, dummy data and database design decisions |
| Software Engineer | Dramane Bako | Python Streamlit interface, database connection, query execution and application pages |
| Tester | All group members | Functional testing, query validation, screenshots, video checks and final review |

## Technology stack

- DBMS: SQLite
- Database file: `database/university.db`
- Programming language: Python
- Interface: Streamlit
- Data display: Pandas/DataFrame tables
- Source control: GitHub
- Report: Microsoft Word using the University of Liverpool template
- Video: MP4 screen recording

## Repository structure

```text
src/                Python source code and Streamlit pages
database/           SQLite database, SQL scripts and database assets
docs/               Report, ERD, screenshots and supporting documentation
meeting_minutes/    Group meeting minutes and milestone records
tests/              Integration tests and validation evidence
video/              Demo video script or final video file
```

## Main features

The current application includes:

- Dashboard summary counts for students, lecturers, courses and departments.
- Student listing and student profile access.
- Lecturer listing and lecturer profile access.
- Non-academic staff listing.
- Course listing and course details.
- Department summary page.
- Programme summary and course requirements.
- Research project listing and project details.
- Query Builder with predefined SQL queries.
- Reports page for management-style summaries.
- CSV export option for query results.

## Query Builder functionality

The Query Builder demonstrates that the Python interface executes SQL queries against the SQLite database. The implemented queries include:

1. Students by Department
2. Students Enrolled in a Course
3. Courses Taught by a Lecturer
4. Lecturers in a Research Area
5. Students by Year of Study
6. Research Projects by Status
7. High-Performing Students
8. Course Enrolment Counts
9. Publications Since a Date
10. Staff by Employment Type

These queries support the assignment requirement to allow users to execute at least five database queries through the Python code.

## Run the app

The repository includes the backend SQLite database at:

```text
database/university.db
```

The app should therefore connect to the real database automatically. When the connection is successful, the sidebar displays:

```text
Connected to database/university.db
```

If this message appears, the app is using the real database rather than in-memory demo data.

---

## Mac instructions

Open Terminal and move into the repository root folder.

```bash
cd ~/Downloads/university-record-management-system-main
```

If your repository is saved somewhere else, replace the path with the correct folder location.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
python3 -m pip install -r src/requirements.txt
```

Start the Streamlit app:

```bash
python3 -m streamlit run src/Dashboard.py
```

The app should open in the browser. If it does not open automatically, copy the local URL shown in Terminal, usually:

```text
http://localhost:8501
```

---

## Windows PowerShell instructions

Open Windows PowerShell and move into the repository root folder.

```powershell
cd C:\Users\<you>\university-record-management-system
```

Replace the path with wherever the repository has been saved.

Install the required packages:

```powershell
py -m pip install -r src/requirements.txt
```

Start the Streamlit app:

```powershell
py -m streamlit run src/Dashboard.py
```

The app should open in the browser. If it does not open automatically, copy the local URL shown in PowerShell, usually:

```text
http://localhost:8501
```

---

## Run the test suite

To confirm that the Python query layer connects correctly to the SQLite database, run:

### Mac

```bash
python3 -m unittest tests.test_database_integration -v
```

### Windows PowerShell

```powershell
py -m unittest tests.test_database_integration -v
```

Expected result:

```text
Ran 6 tests ... OK
```

The tests check that the database file exists, the app can connect to it, and the main query functions execute against the backend schema.


## Notes

- Do not delete `database/university.db`, because the app uses it as the live backend database.
- If the sidebar says demo data is being used, check that `database/university.db` is still present.
- Keep the final repository and submission files consistent across all group members.
