import mysql.connector
import csv
import re

def connect():
	try:
		sql = mysql.connector.connect(host="localhost", database="test", user="root", password="")
		if sql.is_connected():
			print("Sucessfully connected to database.")
			cur = sql.cursor()
			return(sql, cur)
	except:
		print("Error connecting to database.")
		exit()

sql, cur = connect()

file = open("Report.html", "w")

html_header = "<!DOCTYPE html><html><head></head><body>"
html_footer = "</body></html>"
html_row = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>"

# o Calling and outputting as a single HTML page for each of the views (i.e. a SELECT * for both views)
# o Format the views as tables.
file.write(html_header)

cur.execute("SELECT * FROM over25Contacts;")
result = cur.fetchall()
file.write("<table border='1px'><tr>")
file.write("<td>Animal Name</td><td>DNA</td><td>Number of Contacts</td></tr>")
for row in result:
	file.write(html_row % (row[0], row[1], row[2]))
file.write("</table>")


html_row = "<tr><td>%s</td><td>%s</td></tr>"
cur.execute("SELECT * FROM numberOfMorphologies;")
result = cur.fetchall()

file.write("<table border='1px'><tr>")
file.write("<td>Animal Name</td><td>Number of Morphologies</td></tr>")

for row in result:
	file.write(html_row % (row[0], row[1]))

file.write("</table>")

# o In the same HTML page, calling and outputting the results of the procedures
results = cur.callproc('getAnimalWithMostContacts', [0])
file.write("<br />The animal with the most number of contacts is <b>"+results[0]+ "</b>.<br />")

results = cur.callproc('getAnimalWithMostMorphologies', [0])
file.write("<br />The animal with the most number of morphologies is <b>"+results[0]+ "</b>.<br />")

file.write(html_footer)
file.close()
sql.close()