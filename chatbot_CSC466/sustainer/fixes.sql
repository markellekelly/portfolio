H Times
UPDATE Schedule SET StartTime = LEFT(StartTime,length(StartTime)-2) WHERE StartTime LIKE '%A';
UPDATE Schedule SET EndTime = LEFT(StartTime,length(EndTime)-2) WHERE EndTime LIKE '%A';
update Schedule set StartTime = CONCAT((LEFT(StartTime,2) + 12),RIGHT(StartTime,8)) where StartTime LIKE '%P' and StartTime not like '12%';
update Schedule set EndTime = CONCAT((LEFT(EndTime,2) + 12),RIGHT(EndTime,8)) where EndTime LIKE '%P' and EndTime not like '12%';
UPDATE Schedule SET StartTime = LEFT(StartTime,length(StartTime)-2) WHERE StartTime LIKE '%P';
UPDATE Schedule SET EndTime = LEFT(StartTime,length(EndTime)-2) WHERE EndTime LIKE '%P';

-- Fix Office Locations
update Schedule set Locations=RIGHT(Locations,length(Locations)-1) where Locations like '0%';
UPDATE Schedule Set Locations=REPLACE(Locations, '-0', '-');
UPDATE Schedule Set Locations=REPLACE(Locations, '-0', '-');

-- Fix VonMigler
UPDATE degrees set university='Oregon State University' where university='CS, Oregon State';
UPDATE degrees set university='California Polytechnic State University, San Luis Obispo' where university='Math, Cal Poly';

DELETE FROM courses WHERE course NOT LIKE 'CSC%' and course NOT LIKE 'CPE%' and course NOT LIKE 'DATA%';
UPDATE instructors set FirstName="Zoe" where HEX(FirstName)="5A6FEB";
UPDATE courses set FirstName="Zoe" where HEX(FirstName)="5A6FEB";
UPDATE researchinterests set FirstName="Zoe" where HEX(FirstName)="5A6FEB";
UPDATE degrees set FirstName="Zoe" where HEX(FirstName)="5A6FEB";
UPDATE seniorprojects set FirstName="Zoe" where HEX(FirstName)="5A6FEB";
UPDATE tenureinformation set FirstName="Zoe" where HEX(FirstName)="5A6FEB";
UPDATE publications set FirstName="Zoe" where HEX(FirstName)="5A6FEB";
UPDATE publications set FirstName="Zoe" where FirstName='Z.';
UPDATE degrees set degreetype=RIGHT(degreetype,LENGTH(degreetype)-1) where degreetype like ' %';
UPDATE     instructors SET     url = CASE url WHEN '' THEN NULL ELSE url END;

UPDATE degrees set degreetype=RIGHT(degreetype,LENGTH(degreetype)-1) where degreetype like ' %';
ALTER TABLE degrees CHANGE Year startdate CHAR(4);
ALTER TABLE degrees ADD COLUMN enddate CHAR(4) AFTER startdate;
update degrees set enddate=startdate;

SELECT DISTINCT(Courses,courseName) from courses;
UPDATE Schedule t1 INNER JOIN courses t2 on t1.Courses = t2.Courses set t1.courseName = t2.courseName;

UPDATE publications set papername=CONVERT(papername USING utf);
UPDATE publications set papername=CONVERT(papername USING ASCII);
ALTER TABLE Schedule MODIFY Year INT UNSIGNED NOT NULL;
ALTER TABLE Schedule change year Year INT UNSIGNED NOT NULL;
ALTER TABLE degrees MODIFY enddate INT UNSIGNED NOT NULL;
ALTER TABLE tenureinformation MODIFY enddate INT UNSIGNED NULL;
ALTER TABLE tenureinformation MODIFY startdate INT UNSIGNED NOT NULL;
UPDATE tenureinformation set enddate = null where enddate = 0;



