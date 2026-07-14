-- Dummy data

INSERT INTO faculties (faculty_id, faculty_name) VALUES
(1, 'Faculty of Science'),
(2, 'Faculty of Engineering'),
(3, 'Faculty of Business and Informatics');

INSERT INTO departments (department_id, department_name, faculty_id, office_location) VALUES
(1, 'Computer Science', 1, 'Science Block A'),
(2, 'Mathematics', 1, 'Science Block B'),
(3, 'Information Systems', 3, 'Informatics Building');

INSERT INTO research_areas (research_area_id, area_name, description) VALUES
(1, 'Artificial Intelligence', 'Machine learning, intelligent agents, and applied AI systems'),
(2, 'Databases', 'Relational databases, data modelling, and transaction processing'),
(3, 'Cybersecurity', 'Network security, secure coding, and digital forensics'),
(4, 'Networks', 'Computer networks, routing, and distributed systems'),
(5, 'Software Engineering', 'Software design, testing, requirements, and project management'),
(6, 'Data Mining', 'Pattern discovery and analytics from large datasets');

INSERT INTO department_research_areas (department_id, research_area_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
(2, 6),
(3, 2), (3, 5), (3, 6);

INSERT INTO programs (program_id, program_name, degree_awarded, duration_years, department_id, enrollment_details) VALUES
(1, 'BSc Computer Science', 'Bachelor of Science', 4, 1, 'Full-time undergraduate program'),
(2, 'BSc Information Systems', 'Bachelor of Science', 3, 3, 'Full-time undergraduate program'),
(3, 'MSc Data Science', 'Master of Science', 2, 1, 'Postgraduate taught program');

INSERT INTO lecturers (lecturer_id, lecturer_number, first_name, last_name, department_id, email, phone, course_load_hours, employment_status) VALUES
(1, 'L001', 'Alice', 'Ndlovu', 1, 'alice.ndlovu@university.edu', '+2305001001', 12, 'Active'),
(2, 'L002', 'Ravi', 'Patel', 1, 'ravi.patel@university.edu', '+2305001002', 10, 'Active'),
(3, 'L003', 'Maria', 'Chen', 2, 'maria.chen@university.edu', '+2305001003', 8, 'Active'),
(4, 'L004', 'Samira', 'Khan', 3, 'samira.khan@university.edu', '+2305001004', 9, 'Active'),
(5, 'L005', 'Thabo', 'Mensah', 1, 'thabo.mensah@university.edu', '+2305001005', 14, 'Active');

INSERT INTO lecturer_qualifications (qualification_id, lecturer_id, qualification_name, institution, year_awarded) VALUES
(1, 1, 'PhD Artificial Intelligence', 'University of Cape Town', 2014),
(2, 1, 'MSc Computer Science', 'University of Mauritius', 2009),
(3, 2, 'PhD Database Systems', 'University of Leeds', 2016),
(4, 3, 'PhD Applied Mathematics', 'National University of Singapore', 2012),
(5, 4, 'PhD Information Systems', 'University of Pretoria', 2015),
(6, 5, 'MSc Software Engineering', 'University of Ghana', 2018);

INSERT INTO lecturer_expertise (lecturer_id, research_area_id, expertise_level) VALUES
(1, 1, 'Expert'), (1, 6, 'Advanced'),
(2, 2, 'Expert'), (2, 5, 'Advanced'),
(3, 6, 'Expert'),
(4, 3, 'Expert'), (4, 5, 'Advanced'),
(5, 4, 'Advanced'), (5, 5, 'Expert');

INSERT INTO lecturer_research_interests (lecturer_id, research_area_id, interest_note) VALUES
(1, 1, 'Ethical AI for education'),
(1, 6, 'Predictive analytics for student success'),
(2, 2, 'Distributed transaction processing'),
(2, 5, 'DevOps and database release practices'),
(3, 6, 'Mathematical models for pattern discovery'),
(4, 3, 'Secure information systems'),
(5, 5, 'Testing and maintainable software architectures');

INSERT INTO courses (course_id, course_code, course_name, description, department_id, level, credits) VALUES
(1, 'CS101', 'Introduction to Programming', 'Programming fundamentals using Python', 1, 1, 15),
(2, 'CS201', 'Data Structures', 'Lists, trees, graphs, and algorithm analysis', 1, 2, 15),
(3, 'CS301', 'Database Systems', 'Relational design, SQL, transactions, and normalization', 1, 3, 15),
(4, 'CS401', 'Artificial Intelligence', 'Search, machine learning, and AI applications', 1, 4, 15),
(5, 'IS201', 'Systems Analysis and Design', 'Business process modelling and requirements analysis', 3, 2, 15),
(6, 'MATH101', 'Calculus I', 'Limits, derivatives, and integrals', 2, 1, 12),
(7, 'CS350', 'Cybersecurity Fundamentals', 'Security principles, threats, and controls', 1, 3, 15);

INSERT INTO program_course_requirements (program_id, course_id, requirement_type, recommended_year, minimum_grade_percent) VALUES
(1, 1, 'Core', 1, 50),
(1, 2, 'Core', 2, 50),
(1, 3, 'Core', 3, 50),
(1, 4, 'Core', 4, 50),
(1, 7, 'Elective', 3, 50),
(2, 1, 'Core', 1, 50),
(2, 5, 'Core', 2, 50),
(2, 3, 'Elective', 3, 50),
(3, 3, 'Core', 1, 50),
(3, 4, 'Core', 1, 50),
(3, 6, 'Elective', 1, 50);

INSERT INTO course_prerequisites (course_id, prerequisite_course_id) VALUES
(2, 1),
(3, 2),
(4, 2),
(7, 2);

INSERT INTO course_materials (material_id, course_id, title, material_type, material_url) VALUES
(1, 1, 'Python Programming Lab Manual', 'Lab Manual', 'https://example.edu/materials/cs101-lab'),
(2, 3, 'Database Normalization Slides', 'Slide Deck', 'https://example.edu/materials/cs301-normalization'),
(3, 3, 'Sample University ERD Dataset', 'Dataset', 'https://example.edu/materials/cs301-dataset'),
(4, 4, 'AI Search Algorithms Video', 'Video', 'https://example.edu/materials/cs401-search'),
(5, 7, 'Cybersecurity Controls Reading Pack', 'Book', 'https://example.edu/materials/cs350-controls');

INSERT INTO semesters (semester_id, academic_year, term, start_date, end_date, is_current) VALUES
(1, 2025, 'Semester 2', '2025-08-01', '2025-12-15', 0),
(2, 2026, 'Semester 1', '2026-02-01', '2026-06-15', 1),
(3, 2026, 'Semester 2', '2026-08-01', '2026-12-15', 0);

INSERT INTO course_offerings (offering_id, course_id, semester_id, schedule, capacity) VALUES
(1, 1, 2, 'Mon 09:00-11:00, Wed 09:00-10:00', 120),
(2, 2, 2, 'Tue 10:00-12:00, Thu 10:00-11:00', 90),
(3, 3, 2, 'Mon 13:00-15:00, Wed 13:00-14:00', 80),
(4, 4, 2, 'Tue 14:00-16:00, Thu 14:00-15:00', 60),
(5, 5, 2, 'Fri 09:00-12:00', 70),
(6, 6, 2, 'Mon 11:00-13:00, Wed 11:00-12:00', 100),
(7, 7, 2, 'Fri 13:00-16:00', 60),
(8, 3, 1, 'Mon 13:00-15:00, Wed 13:00-14:00', 80),
(9, 1, 1, 'Tue 09:00-12:00', 120);

INSERT INTO teaching_assignments (offering_id, lecturer_id, teaching_role) VALUES
(1, 5, 'Lead Lecturer'),
(2, 5, 'Lead Lecturer'),
(3, 2, 'Lead Lecturer'),
(3, 1, 'Co-Lecturer'),
(4, 1, 'Lead Lecturer'),
(5, 4, 'Lead Lecturer'),
(6, 3, 'Lead Lecturer'),
(7, 4, 'Lead Lecturer'),
(7, 5, 'Co-Lecturer'),
(8, 2, 'Lead Lecturer'),
(9, 5, 'Lead Lecturer');

INSERT INTO students (student_id, student_number, first_name, last_name, date_of_birth, program_id, year_of_study, enrollment_year, graduation_status) VALUES
(1, 'S001', 'John', 'Smith', '2003-05-12', 1, 4, 2022, 'Eligible'),
(2, 'S002', 'Aisha', 'Khan', '2003-09-20', 1, 4, 2022, 'Not Graduated'),
(3, 'S003', 'Brian', 'Lee', '2005-02-03', 1, 2, 2024, 'Not Graduated'),
(4, 'S004', 'Grace', 'Dlamini', '2004-11-18', 2, 3, 2023, 'Eligible'),
(5, 'S005', 'Omar', 'Hassan', '2003-01-31', 1, 4, 2022, 'Not Graduated'),
(6, 'S006', 'Mei', 'Wong', '2001-07-08', 3, 1, 2026, 'Not Graduated'),
(7, 'S007', 'Jacob', 'Nkomo', '2004-04-25', 2, 3, 2023, 'Deferred');

INSERT INTO student_contacts (contact_id, student_id, contact_type, contact_value, is_primary) VALUES
(1, 1, 'Email', 'john.smith@student.university.edu', 1),
(2, 1, 'Phone', '+2305700001', 1),
(3, 2, 'Email', 'aisha.khan@student.university.edu', 1),
(4, 2, 'Phone', '+2305700002', 1),
(5, 3, 'Email', 'brian.lee@student.university.edu', 1),
(6, 4, 'Email', 'grace.dlamini@student.university.edu', 1),
(7, 5, 'Email', 'omar.hassan@student.university.edu', 1),
(8, 6, 'Email', 'mei.wong@student.university.edu', 1),
(9, 7, 'Email', 'jacob.nkomo@student.university.edu', 1),
(10, 7, 'Emergency Contact', 'Nomsa Nkomo +2305800999', 0);

INSERT INTO student_advisors (student_id, lecturer_id, start_date, end_date) VALUES
(1, 1, '2024-01-15', NULL),
(2, 2, '2024-01-15', NULL),
(3, 5, '2024-02-01', NULL),
(4, 4, '2023-02-01', NULL),
(5, 1, '2024-01-15', NULL),
(6, 2, '2026-02-01', NULL),
(7, 4, '2023-02-01', NULL);

INSERT INTO disciplinary_records (disciplinary_record_id, student_id, incident_date, description, action_taken, status) VALUES
(1, 3, '2025-10-12', 'Late submission of academic integrity declaration', 'Written warning issued', 'Resolved'),
(2, 7, '2026-03-20', 'Repeated absence from compulsory lab sessions', 'Meeting with program coordinator', 'Open');

INSERT INTO student_organizations (organization_id, organization_name, department_id, description) VALUES
(1, 'Computing Society', 1, 'Student organization for computing events'),
(2, 'Cybersecurity Club', 1, 'Security workshops and competitions'),
(3, 'Data Science Forum', 1, 'Analytics and data science seminars'),
(4, 'Business Tech Association', 3, 'Information systems and business technology events');

INSERT INTO student_organization_registrations (registration_id, student_id, organization_id, role_title, registered_date, active) VALUES
(1, 1, 1, 'Treasurer', '2025-02-10', 1),
(2, 2, 2, 'Member', '2025-02-12', 1),
(3, 3, 1, 'Member', '2026-02-15', 1),
(4, 4, 4, 'Secretary', '2025-03-01', 1),
(5, 5, 3, 'Member', '2025-05-05', 1),
(6, 6, 3, 'Member', '2026-03-04', 1);

INSERT INTO enrollments (enrollment_id, student_id, offering_id, enrollment_date, enrollment_status, final_grade_percent) VALUES
(1, 1, 3, '2026-02-05', 'Enrolled', 78),
(2, 1, 4, '2026-02-05', 'Enrolled', 82),
(3, 2, 3, '2026-02-06', 'Enrolled', 68),
(4, 2, 7, '2026-02-06', 'Enrolled', 72),
(5, 3, 2, '2026-02-07', 'Enrolled', 61),
(6, 3, 6, '2026-02-07', 'Enrolled', 66),
(7, 4, 5, '2026-02-05', 'Enrolled', 75),
(8, 4, 3, '2026-02-05', 'Enrolled', 71),
(9, 5, 4, '2026-02-08', 'Enrolled', 88),
(10, 5, 7, '2026-02-08', 'Enrolled', 84),
(11, 6, 3, '2026-02-08', 'Enrolled', 79),
(12, 1, 8, '2025-08-03', 'Completed', 76),
(13, 2, 8, '2025-08-03', 'Completed', 65),
(14, 7, 9, '2025-08-03', 'Completed', 58);

INSERT INTO grade_items (grade_item_id, enrollment_id, assessment_name, score_percent, weight_percent, graded_on) VALUES
(1, 1, 'Assignment 1', 80, 20, '2026-03-01'),
(2, 1, 'Midterm Test', 76, 30, '2026-04-01'),
(3, 1, 'Final Project', 78, 50, '2026-06-01'),
(4, 2, 'Lab Portfolio', 84, 30, '2026-03-15'),
(5, 2, 'AI Project', 82, 40, '2026-05-01'),
(6, 2, 'Final Exam', 80, 30, '2026-06-07'),
(7, 3, 'Assignment 1', 70, 20, '2026-03-01'),
(8, 3, 'Midterm Test', 66, 30, '2026-04-01'),
(9, 4, 'Security Lab', 74, 40, '2026-04-15'),
(10, 5, 'Data Structures Lab', 62, 40, '2026-03-20'),
(11, 6, 'Calculus Test', 66, 50, '2026-04-10'),
(12, 7, 'Requirements Report', 75, 50, '2026-04-18'),
(13, 8, 'Database Case Study', 71, 50, '2026-05-02'),
(14, 9, 'AI Project', 90, 50, '2026-05-04'),
(15, 10, 'Cybersecurity Audit', 84, 50, '2026-05-10'),
(16, 11, 'Database Design Project', 79, 60, '2026-05-12');

INSERT INTO committees (committee_id, committee_name, department_id, purpose) VALUES
(1, 'Curriculum Committee', 1, 'Review program course requirements'),
(2, 'Research Ethics Committee', NULL, 'Review research ethics applications'),
(3, 'Assessment Moderation Committee', 3, 'Moderate assessments and marking standards');

INSERT INTO committee_memberships (committee_id, lecturer_id, role_title, start_date, end_date) VALUES
(1, 2, 'Chair', '2025-01-10', NULL),
(1, 5, 'Member', '2025-01-10', NULL),
(2, 1, 'Member', '2025-03-01', NULL),
(2, 3, 'Member', '2025-03-01', NULL),
(3, 4, 'Chair', '2025-02-01', NULL);

INSERT INTO research_groups (research_group_id, group_name, department_id, head_lecturer_id, description) VALUES
(1, 'AI and Learning Analytics Lab', 1, 1, 'Applied AI and student success analytics'),
(2, 'Data Systems Group', 1, 2, 'Database systems and reliable data platforms'),
(3, 'Secure Information Systems Group', 3, 4, 'Cybersecurity and information assurance');

INSERT INTO publications (publication_id, title, publication_type, venue, publication_date, publication_year, doi) VALUES
(1, 'Learning Analytics Models for Early Intervention', 'Journal', 'Journal of Educational Data Science', '2026-02-10', 2026, '10.1000/learn-analytics-2026'),
(2, 'Optimizing Transaction Logs in Teaching Databases', 'Conference', 'International Conference on Database Education', '2025-11-18', 2025, '10.1000/db-logs-2025'),
(3, 'Secure Requirements Engineering for University Systems', 'Journal', 'Information Systems Security Review', '2026-04-12', 2026, '10.1000/secure-req-2026'),
(4, 'Graph Mining Methods for Student Pathways', 'Conference', 'Data Mining Africa', '2025-06-30', 2025, '10.1000/graph-mining-2025'),
(5, 'Maintainable Software Architectures in Higher Education', 'Report', 'University Technical Reports', '2024-10-10', 2024, '10.1000/software-arch-2024');

INSERT INTO lecturer_publications (lecturer_id, publication_id, author_order) VALUES
(1, 1, 1),
(1, 4, 2),
(2, 2, 1),
(4, 3, 1),
(5, 5, 1),
(3, 4, 1);

INSERT INTO research_projects (project_id, project_title, principal_investigator_id, research_group_id, start_date, end_date, project_status) VALUES
(1, 'AI Advising for Student Success', 1, 1, '2025-02-01', NULL, 'Active'),
(2, 'Reliable Course Enrollment Database', 2, 2, '2025-08-01', NULL, 'Active'),
(3, 'Secure Student Portal Redesign', 4, 3, '2025-05-01', '2026-06-30', 'Completed'),
(4, 'Software Testing Automation for University Apps', 5, NULL, '2026-01-10', NULL, 'Active');

INSERT INTO funding_sources (funding_source_id, source_name, source_type) VALUES
(1, 'National Research Fund', 'Government'),
(2, 'University Innovation Grant', 'University'),
(3, 'TechCorp Education Partnership', 'Industry'),
(4, 'African Digital Learning Initiative', 'International');

INSERT INTO project_funding (project_id, funding_source_id, amount, grant_reference) VALUES
(1, 1, 750000, 'NRF-AI-2025-01'),
(1, 4, 400000, 'ADLI-2025-EDU'),
(2, 2, 250000, 'UIG-DB-2025'),
(3, 3, 500000, 'TECH-SEC-2025'),
(4, 2, 200000, 'UIG-TEST-2026');

INSERT INTO project_team_members (project_team_member_id, project_id, student_id, lecturer_id, staff_id, member_role) VALUES
(1, 1, NULL, 1, NULL, 'Principal Investigator'),
(2, 1, 1, NULL, NULL, 'Student Researcher'),
(3, 1, 5, NULL, NULL, 'Student Researcher'),
(4, 2, NULL, 2, NULL, 'Principal Investigator'),
(5, 2, 6, NULL, NULL, 'Graduate Research Assistant'),
(6, 3, NULL, 4, NULL, 'Principal Investigator'),
(7, 3, 4, NULL, NULL, 'Student Researcher'),
(8, 4, NULL, 5, NULL, 'Principal Investigator'),
(9, 4, 3, NULL, NULL, 'Student Tester');

INSERT INTO project_publications (project_id, publication_id) VALUES
(1, 1),
(1, 4),
(2, 2),
(3, 3),
(4, 5);

INSERT INTO project_outcomes (outcome_id, project_id, outcome_type, description, outcome_date) VALUES
(1, 1, 'Prototype', 'Prototype advisor dashboard for identifying at-risk students', '2026-05-20'),
(2, 2, 'Software', 'Enrollment database proof of concept', '2026-03-15'),
(3, 3, 'Report', 'Security redesign recommendations for the student portal', '2026-06-20'),
(4, 4, 'Software', 'Automated test scripts for student record workflows', '2026-06-05');

INSERT INTO student_research_supervision (supervision_id, student_id, lecturer_id, project_id, supervision_role, start_date, end_date) VALUES
(1, 1, 1, 1, 'Supervisor', '2025-02-01', NULL),
(2, 5, 1, 1, 'Supervisor', '2025-02-01', NULL),
(3, 6, 2, 2, 'Supervisor', '2025-08-01', NULL),
(4, 4, 4, 3, 'Supervisor', '2025-05-01', '2026-06-30'),
(5, 3, 5, 4, 'Supervisor', '2026-01-10', NULL),
(6, 2, 2, 2, 'Co-Supervisor', '2026-02-01', NULL);

INSERT INTO non_academic_staff (staff_id, staff_number, first_name, last_name, job_title, department_id, employment_type, email, phone) VALUES
(1, 'N001', 'Priya', 'Naidoo', 'Department Administrator', 1, 'Full-time', 'priya.naidoo@university.edu', '+2305200001'),
(2, 'N002', 'Daniel', 'Mokoena', 'IT Support Officer', 1, 'Full-time', 'daniel.mokoena@university.edu', '+2305200002'),
(3, 'N003', 'Farah', 'Ali', 'Laboratory Technician', 2, 'Contract', 'farah.ali@university.edu', '+2305200003'),
(4, 'N004', 'Jean', 'Morel', 'Program Coordinator', 3, 'Full-time', 'jean.morel@university.edu', '+2305200004');

INSERT INTO staff_contracts (contract_id, staff_id, contract_start_date, contract_end_date, contract_details, salary_amount, salary_currency) VALUES
(1, 1, '2024-01-01', NULL, 'Permanent administrative contract', 52000, 'MUR'),
(2, 2, '2024-03-01', NULL, 'Permanent IT support contract', 48000, 'MUR'),
(3, 3, '2026-01-01', '2026-12-31', 'One-year laboratory support contract', 36000, 'MUR'),
(4, 4, '2023-07-01', NULL, 'Permanent program coordination contract', 55000, 'MUR');

INSERT INTO staff_emergency_contacts (emergency_contact_id, staff_id, contact_name, relationship, phone, email) VALUES
(1, 1, 'Anil Naidoo', 'Spouse', '+2305900001', 'anil.naidoo@example.com'),
(2, 2, 'Lebo Mokoena', 'Sibling', '+2305900002', 'lebo.mokoena@example.com'),
(3, 3, 'Nadia Ali', 'Parent', '+2305900003', 'nadia.ali@example.com'),
(4, 4, 'Claire Morel', 'Spouse', '+2305900004', 'claire.morel@example.com');

INSERT INTO student_employment (student_employment_id, student_id, department_id, supervisor_staff_id, job_title, start_date, end_date, hourly_rate) VALUES
(1, 1, 1, 1, 'Teaching Office Assistant', '2026-02-15', NULL, 250),
(2, 3, 1, 2, 'Computer Lab Assistant', '2026-02-20', NULL, 220),
(3, 4, 3, 4, 'Program Office Assistant', '2026-03-01', NULL, 230),
(4, 6, 1, 1, 'Research Data Assistant', '2026-03-10', NULL, 260);
