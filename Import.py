# -*- coding: utf-8 -*-
import mysql.connector
import csv
import re

def connect():
	try:
		sql = mysql.connector.connect(host="localhost", database="test", user="root", password="")
		#sql = mysql.connector.connect(host="wsp-bict01.usc.internal", database="ict320_s2_19_e_g048_task2", user="ict320-e_g048", password="mysql-e_g048")
		if sql.is_connected():
			print("Sucessfully connected to database.")
			cur = sql.cursor()
			return(sql, cur)
	except:
		print("Error connecting to database.")
		exit()

def commit(sql):
	try:
		sql.commit()
		print("Commited succesfully!")
	except:
		sql.rollback()
		print("Failed to commit, rolled back.")

def insertIndividuals():
	### Insert Individuals.
	print("Inserting individuals.")
	csv_reader = csv.reader(open("Individuals.csv"), delimiter=";")
	#query = "INSERT INTO Individuals (Old_ID, Animal_Name, Photo, Profile, Photo_location, Original_ID_by, Sex, Tagged, Pit_tag, DNA, Sample, CU_Sample, DNA_plate, Well, Notes, Age, General_Location, Date_tagged, Date_DNA_taken, Tag_30_09, Genotyped, Genotyped_sample_no, Extracted, Date_Extracted, Date_Genotyped, Tail, Blood, Skin, Faeces) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	query = "INSERT INTO Individuals VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

	skip_columns = ['TAIL', 'BLOOD', 'SKIN', 'FAECES']
	column_names = []

	row_count = 0
	for row in csv_reader:
		# Store column names.
		if row_count == 0:
			for name in row:
				column_names.append(name)
			row_count += 1
			continue

		item_count = 0
		items = []

		# Collect all row values in items-list.
		for item in row:
			if column_names[item_count] in skip_columns: # Skip specified columns.
				item_count += 1
				continue
			
			if item == '':
				item = None; # Use None instead of '' because integer columns need Null/None.

			# Replace initials with corresponding username.
			if column_names[item_count] == "ORIGINAL ID BY":
				if item != "":
					cur.execute("SELECT username FROM users WHERE initials = '%s'" % item)			
					result = cur.fetchone()
					# If no user matches the initials, use Unknown.
					if result == None:
						item = "U"
						#print("No user matching initials, using Unknown.")
				else:
					item = "U" # If user not defined, use Unknown.
			items.append(item)
			item_count += 1

		# Execute the insert query with the items-list as arguments.
		cur.execute(query, items)
		row_count += 1
	print("Inserted Individuals!")

def insertContacts():
	### Insert Contacts.
	print("Inserting Contacts.")
	csv_reader = csv.reader(open("Contact and Morph.csv"), delimiter=";")
	#query = "INSERT INTO Contacts ('Animal_ID','Contact_Date','Contact_Time','Type','Latitude','Longitude','Location_Sighted','Notes','Field_Record_by','Body_Temp','MORPHOLOGY','GRAVID','DOMINANCE','DB_ENTRY_BY','PHOTO_ID_BY','PHOTO','I3S_Match','I3SS_Manta_Score','PHOTO_QUALITY','LF','LH','UF','UH','HB','AW','TS','CH','F','E','HB_fast','HB_slow','AW_left','AW_right','F_contact','F_non_contact','N','L','M','B','T','R','DEWLAP','DISEASED','TAIL','BLOOD','FAECES','SKIN','HEAMATOLOGY','SWAB_SKIN','SWAB_ORAL','SWAB_CLOACAL') VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
	query = "INSERT INTO Contacts VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
	morph_query = "INSERT INTO Morphologies VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"

	skip_columns = ['CONTACT ID','TORSO CMS', 'JAW WIDTH MMS', 'TAIL GIRTH CMS', 'WEIGHT GMS', 'TAIL LGTH', 'JAW LGTH', 'TAIL', 'BLOOD', 'FAECES', 'SKIN', 'HEAMATOLOGY', 'SWAB - SKIN', 'SWAB - ORAL', 'SWAB CLOACAL']
	morph_columns = ['TORSO CMS', 'JAW WIDTH MMS', 'TAIL GIRTH CMS', 'WEIGHT GMS', 'TAIL LGTH', 'JAW LGTH']
	column_names = []

	row_count = 0
	for row in csv_reader:
		# Store column names.
		if row_count == 0:
			for name in row:
				column_names.append(name)
			row_count += 1
			continue

		item_count = 0
		items = []
		morph_items = []

		# Collect all row values in items-list.
		for item in row:
			if column_names[item_count] == "ANIMAL ID":
				#morph_items.append(item)
				cur.execute("SELECT Animal_Name FROM Individuals WHERE Old_ID = '%s'" % item)
				result = cur.fetchone()
				if result == None:
					print("Skipped row because Animal ID is NULL.")
					break

				items.append(result[0])
				morph_items.append(result[0])
				morph_items.append(row_count)
				item_count += 1
				continue

			if column_names[item_count] in morph_columns: # Skip specified columns.
				#print("SKIPPED", column_names[item_count])
				if item == '':
					item = None; # Use None instead of '' because integer columns need Null/None.
				morph_items.append(item)
				item_count += 1
				continue

			if column_names[item_count] in skip_columns: # Skip specified columns.
				#print("SKIPPED", column_names[item_count])
				if item == '':
					item = None; # Use None instead of '' because integer columns need Null/None.
				item_count += 1
				continue

			if item == '':
				item = None; # Use None instead of '' because integer columns need Null/None.

			# Replace initials with corresponding username.
			if column_names[item_count] == "DB ENTRY BY" or column_names[item_count] == "PHOTO ID BY" or column_names[item_count] == "FIELD RECORD":
				if item != "":
					cur.execute("SELECT username FROM users WHERE initials = '%s'" % item)			
					result = cur.fetchone()
					# If no user matches the initials, use Unknown.
					if result == None:
						item = "U"
						#print("No user matching initials, used Unknown.")
				else:
					item = "U" # If user not defined, use Unknown.

			if column_names[item_count] == "TYPE": # Change input value to uppercase.
				if item != None:
					item = item.upper()

			items.append(item)
			item_count += 1

		if (len(items) != 43):
			continue

		cur.execute(query, items)

		if (items[11] == "TRUE"):
			cur.execute(morph_query, morph_items)

		row_count += 1
	commit(sql)
	print("Inserted contacts!")

### Start.
sql, cur = connect()

# Check if Individuals have already been inserted, if not insert data.
cur.execute(" SELECT Animal_Name FROM Individuals WHERE Animal_Name = 'Acer' ")			
result = cur.fetchone()
if result == None:
	insertIndividuals()
	commit(sql)

#insertIndividuals()
#commit(sql)

# Insert data into Contacts.
insertContacts()
commit(sql)