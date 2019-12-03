import os, sys, random, requests
from bs4 import BeautifulSoup
from nameparser import HumanName
from collections import Counter
import pymysql

logfile = open('sustainerfile.txt','a')
url = "http://catalog.calpoly.edu/facultyandstaff/#facultystaffemeritustext"
myRequest = requests.get(url)
soup = BeautifulSoup(myRequest.text,"html.parser")

full_list = []
for eventRow in soup.find_all('tr'):
   if 'Computer Science' in eventRow.text:
      professor = eventRow.find('td', attrs={'class': 'column0'})
      professor = professor.text.split(' (')[0]
      degree = eventRow.find('td', attrs={'class':'column2'})
      lastcollege = ''
      print(degree)
      for item in degree.text.split(';'):
         count = 0
         a_list = []
         item = item.replace('B.S. ','B.S., ')
         item = item.replace('M.S. ','M.S., ')
         item = item.replace('Ph.D. ','Ph.D., ')
         a_list.append(HumanName(professor).first)
         a_list.append(HumanName(professor).last)
         if item == 'Ph.D., Wichita State University 2017.':
            a_list.append(' Ph.D')
            a_list.append('Wichita State University')
            a_list.append('1999')
         else:
            for an_item in item.split('., '):
               if count == 0:
                  a_list.append(an_item)
               if count == 1:
                  an_item = an_item.replace('.','')
                  if an_item.strip().isdigit():
                     a_list.append(lastcollege)
                     a_list.append(an_item)
                  else:

                     lastcollege = an_item.rsplit(', ',1)[0]
                     a_list.append(an_item.rsplit(', ',1)[0])
                     a_list.append(an_item.rsplit(', ',1)[1])
               count += 1
         full_list.append(a_list)
print(full_list)

try:
   connection = pymysql.connect(
     host="localhost",
     user="jmabel466",
     passwd="****",
     database="jmabel466"
   )

   sql_insert_query = """INSERT INTO degrees (FirstName, LastName, degreetype, university, dyear)
                       VALUES (%s,%s,%s,%s,%s) """
   cursor = connection.cursor()
   result = cursor.executemany(sql_insert_query, full_list)
   connection.commit()
   print(cursor.rowcount, "Record inserted successfully into python_users table")
except pymysql.InternalError as error:
   code, message = error.args
   logfile.write(code, message)
logfile.close()
