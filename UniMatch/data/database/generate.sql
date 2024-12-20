CREATE TABLE IF NOT EXISTS "Areas" (
  "IDArea" INTEGER PRIMARY KEY,
  "AreaName" TEXT
);

CREATE TABLE IF NOT EXISTS "Users" (
  "IDUser" INTEGER PRIMARY KEY,
  "Name" TEXT,
  "Age" INTEGER,
  "Password" TEXT,
  "CountryCode" TEXT,
  "EducationLevel" INTEGER,
  "MainArea" INTEGER,
  FOREIGN KEY("MainArea") REFERENCES "AREAS"("IDArea")
);

CREATE INDEX "ix_Users_IDUser"ON "Users" ("IDUser");

CREATE TABLE IF NOT EXISTS "UserPreferences" (
  "IDPreference" INTEGER PRIMARY KEY,
  "UserID" INTEGER,
  "Preferences" TEXT,
  "Weight" INTEGER,
  FOREIGN KEY("UserID") REFERENCES "Users" ("IDUser")
);

CREATE INDEX "ix_UserPreferences_IDPreference"ON "UserPreferences" ("IDPreference");

CREATE TABLE IF NOT EXISTS "Universities" (
  "IDUniversity" INTEGER PRIMARY KEY,
  "CountryCode" TEXT,
  "UniversityName" TEXT,
  "MainWebsite" TEXT
);

CREATE INDEX "ix_Universities_IDUniversity"ON "Universities" (IDUniversity);

CREATE TABLE IF NOT EXISTS "Courses" (
"IDCourse" INTEGER PRIMARY KEY,
  "IDUniversity" INTEGER,
  "CourseName" TEXT,
  "CourseDescription" TEXT,
  "CourseType" TEXT,
  "Duration" TEXT,
  "Tuition" INTEGER,
  "AcceptsInternationals" INTEGER,
  "Area" INTEGER,
  "Language" TEXT,
  FOREIGN KEY("IDUniversity") REFERENCES "Universities" ("IDUniversity"),
  FOREIGN KEY("Area") REFERENCES "Areas" ("IDArea")
);

CREATE INDEX "ix_Courses_IDCourse"ON "Courses" ("IDCourse");

CREATE TABLE IF NOT EXISTS "Subjects" (
"IDSubject" INTEGER PRIMARY KEY,
  "IDCourse" INTEGER,
  "SubjectName" TEXT,
  "SubjectDescription" TEXT,
  "ECTS" REAL,
  "WeeklyHours" REAL,
  "Semester" REAL,
  FOREIGN KEY("IDCourse") REFERENCES "Courses" ("IDCourse")
);

CREATE INDEX "ix_Subjects_IDSubject"ON "Subjects" ("IDSubject");

CREATE TABLE IF NOT EXISTS "Internationals" (
"IDInternational" INTEGER PRIMARY KEY,
  "IDCourse" INTEGER,
  "Destination" TEXT,
  FOREIGN KEY("IDCourse") REFERENCES "Courses" ("IDCourse")
);

CREATE INDEX "ix_Internationals_IDInternational"ON "Internationals" ("IDInternational");

CREATE TABLE IF NOT EXISTS "Scholarships" (
"IDScholarship" INTEGER PRIMARY KEY,
  "IDCourse" REAL,
  "IDUniversity" INTEGER,
  "ScholarshipName" TEXT,
  "Provider" TEXT,
  "MinAmount" REAL,
  "MaxAmount" REAL,
  "Benefits" TEXT,
  FOREIGN KEY("IDCourse") REFERENCES "Courses" ("IDCourse"),
  FOREIGN KEY("IDUniversity") REFERENCES "Universities" ("IDUniversity")
);

CREATE INDEX "ix_Scholarships_IDScholarship"ON "Scholarships" ("IDScholarship");

CREATE TABLE IF NOT EXISTS "Requisites" (
"IDRequisite" INTEGER PRIMARY KEY,
  "IDCourse" REAL,
  "IDScholarship" REAL,
  "Requisite" TEXT,
  FOREIGN KEY("IDCourse") REFERENCES "Courses" ("IDCourse"),
  FOREIGN KEY("IDScholarship") REFERENCES "Scholarships" ("IDScholarship")
);
