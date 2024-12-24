INSERT INTO universities_search
  SELECT IDUniversity, Country || ' ' || UniversityName
  FROM Universities, Countries
    WHERE UNIVERSITIES.COUNTRYCODE = COUNTRIES.COUNTRYCODE;

INSERT INTO Courses_Search
    SELECT IDCourse, IDUniversity, CourseName || ' ' || CourseDescription || ' ' || CourseType || ' ' || AreaName || ' ' || Language
    FROM Courses, Areas
    WHERE COURSES.AREA = AREAS.IDAREA;
    
INSERT INTO Subjects_Search
    SELECT IDSubject, IDCourse, SubjectName || ' ' || SubjectDescription
    FROM SUBJECTS;

INSERT INTO Internationals_Search
    SELECT IDInternational, IDCourse, Destination
    FROM Internationals;

INSERT INTO Scholarships_Search
    SELECT IDScholarship, ScholarshipName || ' ' || Provider || ' ' || Benefits
    FROM Scholarships;
