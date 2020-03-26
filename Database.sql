# o ALTER/CREATE TABLE statements for:
# ▪ Changes proposed in your redesign from Part A
# ▪ Commands for the missing FOREIGN KEYs, INDEXes and UNIQUEness constraints.

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Samples;
DROP TABLE IF EXISTS Morphologies;
DROP TABLE IF EXISTS Contacts;
DROP TABLE IF EXISTS Individuals;
DROP TABLE IF EXISTS Users;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE Users(
Username VARCHAR(27),
Initials VARCHAR(2),
Superuser VARCHAR(1),
Active VARCHAR(1),

PRIMARY KEY (Initials)
);

INSERT INTO Users VALUES ('Celine Frere', 'CF', 'Y', 'Y' );
INSERT INTO Users VALUES ('Sinta Frere', 'SF', 'Y', 'Y' );
INSERT INTO Users VALUES ('Carme Piza Roca', 'CP', 'N', 'N' );
INSERT INTO Users VALUES ('Bethan Littleford', 'BL', 'N', 'N' );
INSERT INTO Users VALUES ('Dan Nugent', 'DN', 'N', 'N' );
INSERT INTO Users VALUES ('Evie P', 'EP', 'N', 'N' );
INSERT INTO Users VALUES ('Harry McDonald', 'HM', 'N', 'N' );
INSERT INTO Users VALUES ('Kasha Strickland', 'KS', 'N', 'Y' );
INSERT INTO Users VALUES ('Nicola Kent', 'NK', 'N', 'Y' );
INSERT INTO Users VALUES ('Riana Gardiner', 'RG', 'N', 'Y' );
INSERT INTO Users VALUES ('Sarah Ball', 'SB', 'N', 'Y' );
INSERT INTO Users VALUES ('Eric Doran', 'ED', 'N', 'N' );
INSERT INTO Users VALUES ('University Qld Student', 'UQ', 'N', 'N' );
INSERT INTO Users VALUES ('Nicola Peterson', 'NP', 'N', 'N' );
INSERT INTO Users VALUES ('Volunteer', 'V', 'N', 'Y' );
INSERT INTO Users VALUES ('Unknown', 'U', 'N', 'N' ); # Not in original data. For error handling when inserting data from Python and reference is missing.

CREATE TABLE Individuals(
Old_ID INT, # Need to keep for correctly importing and relating all data.
Animal_Name VARCHAR(27),
Photo ENUM('TRUE', 'FALSE'),
Profile ENUM('L', 'R', 'L & R'),
Photo_location ENUM('1','2'),
Original_ID_by VARCHAR(2),
Sex ENUM('M', 'F', 'U') NOT NULL,
Tagged ENUM('TRUE', 'FALSE') NOT NULL,
Pit_tag	BIGINT,
DNA	ENUM('TRUE', 'FALSE'),
Sample TEXT,
CU_Sample TEXT,
DNA_plate TEXT,
Well TEXT,
Notes TEXT,
Age ENUM('Adult', 'Juvenile'),
General_Location ENUM('ARID', 'BBABS', 'BROMS', 'LAKE', 'PGROUND', 'RAINFST', 'SPEC'),
Date_tagged	DATE,
Date_DNA_taken DATE,
Tag_30_09 TEXT,
Genotyped VARCHAR(5),
Genotyped_sample_no INT,
Extracted VARCHAR(5),
Date_Extracted	DATE,
Date_Genotyped	DATE,

PRIMARY KEY (Animal_Name),
FOREIGN KEY (Original_ID_by) REFERENCES Users(Initials)
);
CREATE INDEX DNAtaken ON Individuals(DNA);

CREATE TABLE Contacts(
Contact_ID INT AUTO_INCREMENT,
Animal_Name VARCHAR(27),
Contact_Date DATE,
Contact_Time VARCHAR(9),
Type ENUM('SIGHTING', 'CATCH', ''),
Latitude INT,
Longitude INT,
Location_Sighted ENUM('ARID', 'BBABS', 'BROMS', 'LAKE', 'PGROUND', 'RAINFST', 'SPEC', ''),
Notes TEXT,
Field_Record_by VARCHAR(2),
Body_Temp VARCHAR(12),
MORPHOLOGY ENUM('TRUE', 'FALSE') NOT NULL,
GRAVID ENUM('TRUE', 'FALSE'),
DOMINANCE ENUM('TRUE', 'FALSE'),
DB_ENTRY_BY VARCHAR(2),
PHOTO_ID_BY VARCHAR(2),
PHOTO VARCHAR(22),
I3S_Match VARCHAR(5),
I3SS_Manta_Score VARCHAR(5),
PHOTO_QUALITY VARCHAR(4),
LFL INT,
LHL INT,
UFL INT,
UHL INT,
HB ENUM('TRUE', 'FALSE'),
AW ENUM('TRUE', 'FALSE'),
TS ENUM('TRUE', 'FALSE'),
CH ENUM('TRUE', 'FALSE'),
F ENUM('TRUE', 'FALSE'),
E ENUM('TRUE', 'FALSE'),
HB_fast ENUM('TRUE', 'FALSE'),
HB_slow ENUM('TRUE', 'FALSE'),
AW_left ENUM('TRUE', 'FALSE'),
AW_right ENUM('TRUE', 'FALSE'),
F_contact ENUM('TRUE', 'FALSE'),
F_non_contact ENUM('TRUE', 'FALSE'),
N ENUM('TRUE', 'FALSE'),
L ENUM('TRUE', 'FALSE'),
M ENUM('TRUE', 'FALSE'),
B ENUM('TRUE', 'FALSE'),
T ENUM('TRUE', 'FALSE'),
R ENUM('TRUE', 'FALSE'),
DEWLAP ENUM('TRUE', 'FALSE'),
DISEASED ENUM('TRUE', 'FALSE') NOT NULL,

PRIMARY KEY (Contact_ID),
FOREIGN KEY (Animal_Name) REFERENCES Individuals(Animal_Name),
FOREIGN KEY (DB_ENTRY_BY) REFERENCES Users(Initials),
FOREIGN KEY (Field_Record_by) REFERENCES Users(Initials),
FOREIGN KEY (PHOTO_ID_BY) REFERENCES Users(Initials)
);
CREATE INDEX Morphology ON Contacts(MORPHOLOGY);

CREATE TABLE Morphologies(
Animal_Name VARCHAR(27),
Contact_ID INT,

Jaw_lgth INT,
Torso_cms INT,
Jaw_width_mms INT,
Tail_girth_cms INT,
Weight_gms INT,
Tail_lgth INT,

PRIMARY KEY (Contact_ID),
FOREIGN KEY (Animal_Name) REFERENCES Individuals(Animal_Name),
FOREIGN KEY (Contact_ID) REFERENCES Contacts(Contact_ID)
);


CREATE TABLE Samples(
Sample_ID INT AUTO_INCREMENT,
Contact_ID INT,
Animal_Name VARCHAR(27),
Date_Extracted DATE, # Needed? Already recorded in Contacts.
Extracted_by VARCHAR(2),
DART_Sample_Number INT, # What is this?
Type ENUM('TAIL', 'BLOOD', 'FAECES', 'SKIN', 'HEAMATOLOGY', 'SWAB_SKIN', 'SWAB_ORAL', 'SWAB_CLOACAL'),

PRIMARY KEY (Sample_ID),
FOREIGN KEY (Contact_ID) REFERENCES Contacts(Contact_ID),
FOREIGN KEY (Extracted_by) REFERENCES Users(Initials),
FOREIGN KEY (Animal_Name) REFERENCES Individuals(Animal_Name)
);

DROP VIEW IF EXISTS over25Contacts;
CREATE VIEW over25Contacts
AS
SELECT Contacts.Animal_Name, DNA, COUNT(Contacts.Contact_ID) as NoOfContacts
FROM Individuals, Contacts
WHERE Contacts.Animal_Name = Individuals.Animal_Name
GROUP BY Contacts.Animal_Name
HAVING COUNT(Contacts.Contact_ID) > 25;

DROP PROCEDURE IF EXISTS getAnimalWithMostContacts;
DELIMITER //
	CREATE PROCEDURE getAnimalWithMostContacts(OUT AnimalNameOut VARCHAR(27))
	BEGIN
	SELECT Animal_Name
	INTO @AnimalName
	FROM over25Contacts
	WHERE
	NoOfContacts = (SELECT MAX(NoOfContacts) FROM over25Contacts);
	SET AnimalNameOut := @AnimalName;
END//

DELIMITER ;

#CALL getAnimalWithMostContacts(@AnimalName);
#SELECT @AnimalName;

DROP VIEW IF EXISTS numberOfMorphologies;
CREATE VIEW numberOfMorphologies
AS
SELECT Animal_Name, count(Contact_ID) as NumberOfMorphologies
FROM Contacts
WHERE Morphology = TRUE
GROUP BY Animal_Name;

DROP PROCEDURE IF EXISTS getAnimalWithMostMorphologies;
DELIMITER //
	CREATE PROCEDURE getAnimalWithMostMorphologies(OUT AnimalNameOut VARCHAR(27))
	BEGIN
	SELECT Animal_Name
	INTO @AnimalName
	FROM numberOfMorphologies
	WHERE
	NumberOfMorphologies = (SELECT MAX(NumberOfMorphologies) FROM numberOfMorphologies);
	SET AnimalNameOut := @AnimalName;
END//
DELIMITER ;

#CALL getAnimalWithMostMorphologies(@AnimalName);
#SELECT @AnimalName;