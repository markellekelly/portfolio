DROP TABLE IF EXISTS researchinterests;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS degrees;
DROP TABLE IF EXISTS publications;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS seniorprojects;
DROP TABLE IF EXISTS tenureinformation;
DROP TABLE IF EXISTS clubs;
DROP TABLE IF EXISTS instructors;
DROP TABLE IF EXISTS otherinstructors;

CREATE TABLE researchinterests (
  FirstName VARCHAR(100),
  LastName VARCHAR(100),
  researchinterests VARCHAR(250),

  PRIMARY KEY (FirstName, LastName, researchinterests)
);

CREATE TABLE courses (
  FirstName VARCHAR(100),
  LastName VARCHAR(100),
  course VARCHAR(50),
  averagegrade DECIMAL(3,2)
);

CREATE TABLE ratings (
  FirstName VARCHAR(100),
  LastName VARCHAR(100),
  polyrating DECIMAL(3,2),
  seesdifficulty DECIMAL(3,2),
  presentsclearly DECIMAL(3,2),
  numratings INTEGER,

  PRIMARY KEY (FirstName, LastName)
);

CREATE TABLE degrees (
  FirstName VARCHAR(100),
  LastName VARCHAR(100),
  university VARCHAR(100),
  degreetype VARCHAR(6),
  dyear CHAR(4),

  PRIMARY KEY (FirstName, LastName, university, degreetype)
);

CREATE TABLE instructors (
  FirstName VARCHAR(100),
  LastName VARCHAR(100),
  position VARCHAR(100),
  chair CHAR(1),
  room VARCHAR(100),
  phone VARCHAR(15),
  url VARCHAR(100),
  email VARCHAR(50),

  PRIMARY KEY (FirstName, LastName)
 );

CREATE TABLE publications (
  FirstName VARCHAR(100),
  LastName VARCHAR(100),
  journalname VARCHAR(250),
  papername VARCHAR(250),

  PRIMARY KEY (LastName, FirstName, journalname, papername)
);

CREATE TABLE seniorprojects (
  FirstName VARCHAR(100),
  LastName VARCHAR(100),
  projectname VARCHAR(250),
  studentname VARCHAR(250),

  PRIMARY KEY (LastName, projectname, studentname)
);

CREATE TABLE tenureinformation (
  startdate VARCHAR(5),
  enddate VARCHAR(5),
  FirstName VARCHAR(100),
  LastName VARCHAR(100),
  almamater VARCHAR(250),

  PRIMARY KEY (LastName, FirstName)
);

CREATE TABLE otherinstructors (
  FirstName VARCHAR(100),
  LastName VARCHAR(100),

  PRIMARY KEY (LastName, FirstName)
);

CREATE TABLE clubs (
  clubname VARCHAR(250) PRIMARY KEY,
  FirstName VARCHAR(100),
  LastName VARCHAR(100)
);
