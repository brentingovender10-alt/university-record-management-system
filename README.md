# university-record-management-system
Group B assignment database connection project for a university record management system.

## Project overview

This repository contains the group assignment for the Database Connection Assignment. The project requires the design and implementation of a university record management system, including a relational database, dummy data, a Python interface for querying the database, a written report, meeting minutes and a demonstration video.

## Group roles

| Role | Name | Main responsibilities |
|---|---|---|
| Project Manager | Brentin Govender | Planning, GitHub coordination, meeting minutes, final submission checklist and report quality control |
| Database Designer / Engineer | Dooshina Oolun | ERD, normalisation, schema, dummy data and database queries |
| Software Engineer | Dramane Bako | Python interface, database connection and query execution |
| Tester | To be confirmed/All 3 | Test plan, validation, screenshots and bug reporting |

## Proposed technology stack

- DBMS: To be confirmed, likely...
- Programming language: Python
- Interface: To be confirmed, likely...
- Source control: GitHub
- Report: Microsoft Word using the University of Liverpool template
- Video: MP4 screen recording

## Repository structure

```text
src/                Python source code
database/           SQL scripts, database file and ERD
docs/               Report, screenshots and supporting documentation
meeting_minutes/    Meeting minutes for group milestones
tests/              Test plan, test results and validation evidence
video/              Final demonstration video or video link/instructions
```

## Run the app

The repository ships with the real backend database at
`database/university.db`, so the app connects to it automatically — no database
build step is required. Open **Windows PowerShell** and run the steps below.

**1. Go to the repository root**

```powershell
cd C:\Users\<you>\university-record-management-system
```

Replace the path with wherever you cloned the repository. All following
commands are run from this folder.

**2. Install dependencies**

```powershell
py -m pip install -r src/requirements.txt
```

**3. Start the app**

```powershell
py -m streamlit run src/Dashboard.py
```

The app opens in the browser. Because `database/university.db` is present, the
front end reads from the real backend schema read-only, and the sidebar footer
reads **"Connected to database/university.db"** (not "Demo data"). Use the
sidebar to move between Students, Lecturers, Courses, Departments, Programs,
Research Projects, the Query Builder and Reports.

**4. (Optional) Prove the integration with the test suite**

```powershell
py -m unittest tests.test_database_integration -v
```

This checks that every front-end query and relation name executes against the
backend schema. Expect `Ran 6 tests ... OK`.
