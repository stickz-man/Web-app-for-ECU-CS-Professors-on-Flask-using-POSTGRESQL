-- PostgreSQL database dump

-- Set session characteristics
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Create table commands
CREATE TABLE public."CH" (
    "Prefix" VARCHAR(10),
    "Number" INT,
    "Title" VARCHAR(255),
    "GU" VARCHAR(10),
    "CH" VARCHAR(10),
    "Frequency" VARCHAR(50),
    "Active" TEXT,
    "Description" TEXT,
    "Remarks" TEXT
);

CREATE TABLE public."Department Committee Assignments" (
    "faculty_ID" INT,
    "committee_ID" INT,
    "start_date" TEXT,
    "end_date" TEXT,
    "remarks" TEXT
);

CREATE TABLE public."Department Committee Names" (
    "ID" INT,
    "committee_name" VARCHAR(255),
    "remarks" TEXT
);

CREATE TABLE public."Department Course Directors" (
    "Prefix" VARCHAR(10),
    "Number" INT,
    "CourseDirectorID" INT,
    "Remarks" TEXT
);

CREATE TABLE public."Faculty" (
    "ID" INT,
    "Honorific" VARCHAR(10),
    "First" VARCHAR(50),
    "MI" VARCHAR(5),
    "Last" VARCHAR(50),
    "Email" VARCHAR(100),
    "Phone" VARCHAR(20),
    "Office" VARCHAR(50),
    "Research" TEXT,
    "Rank" VARCHAR(50),
    "Remarks" TEXT,
    "CurrentlyEmployed" TEXT
);

CREATE TABLE public."Prerequisites" (
    "Prefix" VARCHAR(10),
    "Number" INT,
    "PC-prefix" VARCHAR(10),
    "PC-number" INT,
    "PC-code" INT
);

CREATE TABLE public."Schedule History" (
    "Year" INT,
    "Semester" VARCHAR(20),
    "Prefix" VARCHAR(10),
    "Number" INT,
    "Section" VARCHAR(10),
    "CRN" INT,
    "Enrollment" INT,
    "Instructor" VARCHAR(100),
    "Days" VARCHAR(10),
    "BeginTime" INT,
    "EndTime" INT,
    "Remarks" TEXT
);

-- Data import commands, updated paths to /tmp/phase4 directory
COPY public."CH" FROM '/tmp/phase4/3368.dat';
COPY public."Department Committee Assignments" FROM '/tmp/phase4/3363.dat';
COPY public."Department Committee Names" FROM '/tmp/phase4/3364.dat';
COPY public."Department Course Directors" FROM '/tmp/phase4/3365.dat';
COPY public."Faculty" FROM '/tmp/phase4/3362.dat';
COPY public."Prerequisites" FROM '/tmp/phase4/3367.dat';
COPY public."Schedule History" FROM '/tmp/phase4/3366.dat';

-- End of dump


