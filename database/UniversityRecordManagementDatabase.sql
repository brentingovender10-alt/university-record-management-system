DROP VIEW IF EXISTS vw_student_average_grades;
DROP VIEW IF EXISTS vw_current_semester_enrollments;
DROP VIEW IF EXISTS vw_lecturer_publications;

DROP TABLE IF EXISTS student_employment;
DROP TABLE IF EXISTS staff_emergency_contacts;
DROP TABLE IF EXISTS staff_contracts;
DROP TABLE IF EXISTS non_academic_staff;
DROP TABLE IF EXISTS student_research_supervision;
DROP TABLE IF EXISTS project_outcomes;
DROP TABLE IF EXISTS project_publications;
DROP TABLE IF EXISTS project_team_members;
DROP TABLE IF EXISTS project_funding;
DROP TABLE IF EXISTS funding_sources;
DROP TABLE IF EXISTS research_projects;
DROP TABLE IF EXISTS research_groups;
DROP TABLE IF EXISTS committee_memberships;
DROP TABLE IF EXISTS committees;
DROP TABLE IF EXISTS lecturer_publications;
DROP TABLE IF EXISTS publications;
DROP TABLE IF EXISTS lecturer_research_interests;
DROP TABLE IF EXISTS lecturer_expertise;
DROP TABLE IF EXISTS research_areas;
DROP TABLE IF EXISTS lecturer_qualifications;
DROP TABLE IF EXISTS grade_items;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS teaching_assignments;
DROP TABLE IF EXISTS course_offerings;
DROP TABLE IF EXISTS semesters;
DROP TABLE IF EXISTS course_materials;
DROP TABLE IF EXISTS course_prerequisites;
DROP TABLE IF EXISTS program_course_requirements;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS student_organization_registrations;
DROP TABLE IF EXISTS student_organizations;
DROP TABLE IF EXISTS disciplinary_records;
DROP TABLE IF EXISTS student_advisors;
DROP TABLE IF EXISTS student_contacts;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS lecturers;
DROP TABLE IF EXISTS programs;
DROP TABLE IF EXISTS department_research_areas;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS faculties;



-- Core university structure

CREATE TABLE faculties (
    faculty_id INTEGER PRIMARY KEY,
    faculty_name TEXT NOT NULL UNIQUE
);

CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL UNIQUE,
    faculty_id INTEGER NOT NULL,
    office_location TEXT,
    FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE research_areas (
    research_area_id INTEGER PRIMARY KEY,
    area_name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE department_research_areas (
    department_id INTEGER NOT NULL,
    research_area_id INTEGER NOT NULL,
    PRIMARY KEY (department_id, research_area_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (research_area_id) REFERENCES research_areas(research_area_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE programs (
    program_id INTEGER PRIMARY KEY,
    program_name TEXT NOT NULL UNIQUE,
    degree_awarded TEXT NOT NULL,
    duration_years INTEGER NOT NULL CHECK (duration_years > 0),
    department_id INTEGER NOT NULL,
    enrollment_details TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Lecturers and academic staff data

CREATE TABLE lecturers (
    lecturer_id INTEGER PRIMARY KEY,
    lecturer_number TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    course_load_hours INTEGER NOT NULL DEFAULT 0 CHECK (course_load_hours >= 0),
    employment_status TEXT NOT NULL DEFAULT 'Active'
        CHECK (employment_status IN ('Active', 'On Leave', 'Retired', 'Resigned')),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE lecturer_qualifications (
    qualification_id INTEGER PRIMARY KEY,
    lecturer_id INTEGER NOT NULL,
    qualification_name TEXT NOT NULL,
    institution TEXT NOT NULL,
    year_awarded INTEGER CHECK (year_awarded BETWEEN 1900 AND 2100),
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE lecturer_expertise (
    lecturer_id INTEGER NOT NULL,
    research_area_id INTEGER NOT NULL,
    expertise_level TEXT DEFAULT 'Intermediate'
        CHECK (expertise_level IN ('Beginner', 'Intermediate', 'Advanced', 'Expert')),
    PRIMARY KEY (lecturer_id, research_area_id),
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (research_area_id) REFERENCES research_areas(research_area_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE lecturer_research_interests (
    lecturer_id INTEGER NOT NULL,
    research_area_id INTEGER NOT NULL,
    interest_note TEXT,
    PRIMARY KEY (lecturer_id, research_area_id),
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (research_area_id) REFERENCES research_areas(research_area_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE publications (
    publication_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    publication_type TEXT NOT NULL
        CHECK (publication_type IN ('Journal', 'Conference', 'Book Chapter', 'Book', 'Report')),
    venue TEXT,
    publication_date DATE,
    publication_year INTEGER CHECK (publication_year BETWEEN 1900 AND 2100),
    doi TEXT UNIQUE
);

CREATE TABLE lecturer_publications (
    lecturer_id INTEGER NOT NULL,
    publication_id INTEGER NOT NULL,
    author_order INTEGER NOT NULL CHECK (author_order > 0),
    PRIMARY KEY (lecturer_id, publication_id),
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (publication_id) REFERENCES publications(publication_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);


-- Students, contacts, advisors, discipline, organizations

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    student_number TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    program_id INTEGER NOT NULL,
    year_of_study INTEGER NOT NULL CHECK (year_of_study > 0),
    enrollment_year INTEGER NOT NULL CHECK (enrollment_year BETWEEN 1900 AND 2100),
    graduation_status TEXT NOT NULL DEFAULT 'Not Graduated'
        CHECK (graduation_status IN ('Not Graduated', 'Eligible', 'Graduated', 'Deferred')),
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE student_contacts (
    contact_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    contact_type TEXT NOT NULL CHECK (contact_type IN ('Email', 'Phone', 'Address', 'Emergency Contact')),
    contact_value TEXT NOT NULL,
    is_primary INTEGER NOT NULL DEFAULT 0 CHECK (is_primary IN (0, 1)),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE student_advisors (
    student_id INTEGER PRIMARY KEY,
    lecturer_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE disciplinary_records (
    disciplinary_record_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    incident_date DATE NOT NULL,
    description TEXT NOT NULL,
    action_taken TEXT,
    status TEXT NOT NULL DEFAULT 'Open'
        CHECK (status IN ('Open', 'Resolved', 'Appealed')),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE student_organizations (
    organization_id INTEGER PRIMARY KEY,
    organization_name TEXT NOT NULL UNIQUE,
    department_id INTEGER,
    description TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE student_organization_registrations (
    registration_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    organization_id INTEGER NOT NULL,
    role_title TEXT NOT NULL DEFAULT 'Member',
    registered_date DATE NOT NULL,
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    UNIQUE (student_id, organization_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (organization_id) REFERENCES student_organizations(organization_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);


-- Courses, offerings, teaching, enrollments, grades

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_code TEXT NOT NULL UNIQUE,
    course_name TEXT NOT NULL,
    description TEXT,
    department_id INTEGER NOT NULL,
    level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 8),
    credits INTEGER NOT NULL CHECK (credits > 0),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE program_course_requirements (
    program_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    requirement_type TEXT NOT NULL CHECK (requirement_type IN ('Core', 'Elective')),
    recommended_year INTEGER CHECK (recommended_year > 0),
    minimum_grade_percent NUMERIC DEFAULT 50 CHECK (minimum_grade_percent BETWEEN 0 AND 100),
    PRIMARY KEY (program_id, course_id),
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE course_prerequisites (
    course_id INTEGER NOT NULL,
    prerequisite_course_id INTEGER NOT NULL,
    PRIMARY KEY (course_id, prerequisite_course_id),
    CHECK (course_id <> prerequisite_course_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (prerequisite_course_id) REFERENCES courses(course_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE course_materials (
    material_id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    material_type TEXT NOT NULL CHECK (material_type IN ('Book', 'Slide Deck', 'Video', 'Dataset', 'Website', 'Lab Manual')),
    material_url TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE semesters (
    semester_id INTEGER PRIMARY KEY,
    academic_year INTEGER NOT NULL CHECK (academic_year BETWEEN 1900 AND 2100),
    term TEXT NOT NULL CHECK (term IN ('Semester 1', 'Semester 2', 'Summer')),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current INTEGER NOT NULL DEFAULT 0 CHECK (is_current IN (0, 1)),
    UNIQUE (academic_year, term)
);

CREATE TABLE course_offerings (
    offering_id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    semester_id INTEGER NOT NULL,
    schedule TEXT NOT NULL,
    capacity INTEGER CHECK (capacity > 0),
    UNIQUE (course_id, semester_id, schedule),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (semester_id) REFERENCES semesters(semester_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE teaching_assignments (
    offering_id INTEGER NOT NULL,
    lecturer_id INTEGER NOT NULL,
    teaching_role TEXT NOT NULL DEFAULT 'Lead Lecturer'
        CHECK (teaching_role IN ('Lead Lecturer', 'Co-Lecturer', 'Tutor', 'Lab Instructor')),
    PRIMARY KEY (offering_id, lecturer_id),
    FOREIGN KEY (offering_id) REFERENCES course_offerings(offering_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    offering_id INTEGER NOT NULL,
    enrollment_date DATE NOT NULL,
    enrollment_status TEXT NOT NULL DEFAULT 'Enrolled'
        CHECK (enrollment_status IN ('Enrolled', 'Completed', 'Dropped', 'Failed')),
    final_grade_percent NUMERIC CHECK (final_grade_percent BETWEEN 0 AND 100),
    UNIQUE (student_id, offering_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (offering_id) REFERENCES course_offerings(offering_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE grade_items (
    grade_item_id INTEGER PRIMARY KEY,
    enrollment_id INTEGER NOT NULL,
    assessment_name TEXT NOT NULL,
    score_percent NUMERIC NOT NULL CHECK (score_percent BETWEEN 0 AND 100),
    weight_percent NUMERIC NOT NULL CHECK (weight_percent BETWEEN 0 AND 100),
    graded_on DATE,
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(enrollment_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);


-- Committees and research

CREATE TABLE committees (
    committee_id INTEGER PRIMARY KEY,
    committee_name TEXT NOT NULL UNIQUE,
    department_id INTEGER,
    purpose TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE committee_memberships (
    committee_id INTEGER NOT NULL,
    lecturer_id INTEGER NOT NULL,
    role_title TEXT NOT NULL DEFAULT 'Member',
    start_date DATE NOT NULL,
    end_date DATE,
    PRIMARY KEY (committee_id, lecturer_id),
    FOREIGN KEY (committee_id) REFERENCES committees(committee_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE research_groups (
    research_group_id INTEGER PRIMARY KEY,
    group_name TEXT NOT NULL UNIQUE,
    department_id INTEGER NOT NULL,
    head_lecturer_id INTEGER NOT NULL UNIQUE,
    description TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (head_lecturer_id) REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE research_projects (
    project_id INTEGER PRIMARY KEY,
    project_title TEXT NOT NULL UNIQUE,
    principal_investigator_id INTEGER NOT NULL,
    research_group_id INTEGER,
    start_date DATE NOT NULL,
    end_date DATE,
    project_status TEXT NOT NULL DEFAULT 'Active'
        CHECK (project_status IN ('Planning', 'Active', 'Completed', 'Suspended')),
    FOREIGN KEY (principal_investigator_id) REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (research_group_id) REFERENCES research_groups(research_group_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE funding_sources (
    funding_source_id INTEGER PRIMARY KEY,
    source_name TEXT NOT NULL UNIQUE,
    source_type TEXT NOT NULL CHECK (source_type IN ('Government', 'University', 'Industry', 'NGO', 'International'))
);

CREATE TABLE project_funding (
    project_id INTEGER NOT NULL,
    funding_source_id INTEGER NOT NULL,
    amount NUMERIC NOT NULL CHECK (amount >= 0),
    grant_reference TEXT,
    PRIMARY KEY (project_id, funding_source_id),
    FOREIGN KEY (project_id) REFERENCES research_projects(project_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (funding_source_id) REFERENCES funding_sources(funding_source_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE project_team_members (
    project_team_member_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    student_id INTEGER,
    lecturer_id INTEGER,
    staff_id INTEGER,
    member_role TEXT NOT NULL,
    CHECK ((student_id IS NOT NULL) + (lecturer_id IS NOT NULL) + (staff_id IS NOT NULL) = 1),
    FOREIGN KEY (project_id) REFERENCES research_projects(project_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (staff_id) REFERENCES non_academic_staff(staff_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE project_publications (
    project_id INTEGER NOT NULL,
    publication_id INTEGER NOT NULL,
    PRIMARY KEY (project_id, publication_id),
    FOREIGN KEY (project_id) REFERENCES research_projects(project_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (publication_id) REFERENCES publications(publication_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE project_outcomes (
    outcome_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    outcome_type TEXT NOT NULL CHECK (outcome_type IN ('Prototype', 'Dataset', 'Publication', 'Policy Brief', 'Software', 'Report')),
    description TEXT NOT NULL,
    outcome_date DATE,
    FOREIGN KEY (project_id) REFERENCES research_projects(project_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE student_research_supervision (
    supervision_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    lecturer_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    supervision_role TEXT NOT NULL DEFAULT 'Supervisor'
        CHECK (supervision_role IN ('Supervisor', 'Co-Supervisor')),
    start_date DATE NOT NULL,
    end_date DATE,
    UNIQUE (student_id, lecturer_id, project_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (project_id) REFERENCES research_projects(project_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Non-academic staff, contracts, emergency contacts, student employment

CREATE TABLE non_academic_staff (
    staff_id INTEGER PRIMARY KEY,
    staff_number TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    employment_type TEXT NOT NULL CHECK (employment_type IN ('Full-time', 'Part-time', 'Contract', 'Temporary')),
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE staff_contracts (
    contract_id INTEGER PRIMARY KEY,
    staff_id INTEGER NOT NULL,
    contract_start_date DATE NOT NULL,
    contract_end_date DATE,
    contract_details TEXT,
    salary_amount NUMERIC CHECK (salary_amount >= 0),
    salary_currency TEXT NOT NULL DEFAULT 'MUR',
    FOREIGN KEY (staff_id) REFERENCES non_academic_staff(staff_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE staff_emergency_contacts (
    emergency_contact_id INTEGER PRIMARY KEY,
    staff_id INTEGER NOT NULL,
    contact_name TEXT NOT NULL,
    relationship TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    FOREIGN KEY (staff_id) REFERENCES non_academic_staff(staff_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE student_employment (
    student_employment_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    supervisor_staff_id INTEGER NOT NULL,
    job_title TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    hourly_rate NUMERIC CHECK (hourly_rate >= 0),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (supervisor_staff_id) REFERENCES non_academic_staff(staff_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);


-- Views for common reporting queries

CREATE VIEW vw_current_semester_enrollments AS
SELECT
    e.enrollment_id,
    s.student_id,
    s.student_number,
    s.first_name || ' ' || s.last_name AS student_name,
    c.course_code,
    c.course_name,
    sem.academic_year,
    sem.term,
    e.enrollment_status,
    e.final_grade_percent
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN course_offerings co ON co.offering_id = e.offering_id
JOIN courses c ON c.course_id = co.course_id
JOIN semesters sem ON sem.semester_id = co.semester_id
WHERE sem.is_current = 1;

CREATE VIEW vw_student_average_grades AS
SELECT
    s.student_id,
    s.student_number,
    s.first_name || ' ' || s.last_name AS student_name,
    p.program_name,
    s.year_of_study,
    p.duration_years,
    ROUND(AVG(e.final_grade_percent), 2) AS average_grade_percent
FROM students s
JOIN programs p ON p.program_id = s.program_id
JOIN enrollments e ON e.student_id = s.student_id
WHERE e.final_grade_percent IS NOT NULL
  AND e.enrollment_status IN ('Enrolled', 'Completed')
GROUP BY s.student_id, s.student_number, student_name, p.program_name, s.year_of_study, p.duration_years;

CREATE VIEW vw_lecturer_publications AS
SELECT
    l.lecturer_id,
    l.lecturer_number,
    l.first_name || ' ' || l.last_name AS lecturer_name,
    d.department_name,
    p.publication_id,
    p.title,
    p.publication_type,
    p.venue,
    p.publication_date,
    p.publication_year,
    p.doi
FROM lecturer_publications lp
JOIN lecturers l ON l.lecturer_id = lp.lecturer_id
JOIN departments d ON d.department_id = l.department_id
JOIN publications p ON p.publication_id = lp.publication_id;

