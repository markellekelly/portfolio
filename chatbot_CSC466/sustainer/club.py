import os, sys, random, requests
from bs4 import BeautifulSoup
import pymysql.cursors
from collections import Counter
from nameparser import HumanName

logfile = open('sustainerlog.txt','a')
url = "http://www.asi.calpoly.edu/club_directories/listing_bs"
myRequest = requests.get(url)

soup = BeautifulSoup(myRequest.text,"html.parser")

temp = []
for item in soup.findAll('li', attrs={'class':'club_list'}):
    last_field = ''
    num = 0
    club_listing = []
    for fields in item.strings:
        if num == 0:
            name = fields
            club_listing.append(name.strip())
        if last_field == 'Advisor:':
            advisor = fields
            advisor = HumanName(advisor)
            club_listing.append(advisor.first)
            club_listing.append(advisor.last)
        last_field = fields
        num += 1
    if '7x24 Student Club' not in club_listing[0]:
        temp.append(club_listing)

try:
   connection = pymysql.connect(
     host="localhost",
     user="jmabel466",
     passwd="****",
     database="jmabel466"
   )

   sql_insert_query = """INSERT INTO clubs (clubname, FirstName, LastName) 
                       VALUES (%s,%s,%s) """
   cursor = connection.cursor()
   result = cursor.executemany(sql_insert_query, temp)
   connection.commit()
   print(cursor.rowcount, "Record inserted successfully into python_users table")
except pymysql.InternalError as error:
   code, message = error.args
   logfile.write(code, message)
logfile.close()
