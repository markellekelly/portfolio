import os, sys, random, requests
from bs4 import BeautifulSoup
from collections import Counter
from nameparser import HumanName
import pymysql

logfile = open('sustainerlog.txt','a')
a_list = []
for i in range(1,293):
   try:
      url = "https://digitalcommons.calpoly.edu/cpesp/" + str(i)
      myRequest = requests.get(url)

      soup = BeautifulSoup(myRequest.text,"html.parser")
      temp = []
      print("Page Title: ",soup.head.title.get_text().strip())
      temp.append(soup.head.title.get_text().strip())
      for eventRow in soup.find_all('div',attrs={'id':'advisor1'}):
         for element in eventRow.find_all('p'):
            temp.append(element.string.strip())
      while len(temp) < 2:
         temp.append('')
      title_student = temp[0].split('by')
      human_name = HumanName(temp[1])
      temp_list = [title_student[0], title_student[1], human_name.first, human_name.last]
      print(temp_list)
      a_list.append(temp_list)
   except: 
      r = "No response"
      logfile.write('A CPE Senior Project Page Timed Out')
      pass

for i in range(1,146):
   try:
      url = "https://digitalcommons.calpoly.edu/cscsp/" + str(i)
      myRequest = requests.get(url)
      soup = BeautifulSoup(myRequest.text,"html.parser")

      temp = []
      print("Page Title: ",soup.head.title.get_text())
      temp.append(soup.head.title.get_text().strip())
      for eventRow in soup.find_all('div',attrs={'id':'advisor1'}):
         for element in eventRow.find_all('p'):
            temp.append(element.string.strip())
      while len(temp) < 2:
         temp.append('')
      title_student = temp[0].split('by')
      human_name = HumanName(temp[1])
      temp_list = [title_student[0], title_student[1], human_name.first, human_name.last]
      print(temp_list)
      a_list.append(temp_list)
   except: 
      r = "No response"
      logfile.write('A CS Senior Project Page Timed Out')
      pass

print(a_list)
try:
   connection = pymysql.connect(
     host="localhost",
     user="jmabel466",
     passwd="****",
     database="jmabel466",
     charset="utf8mb4"
   )

   sql_insert_query = """INSERT INTO seniorprojects (projectname,studentname,FirstName,LastName)
                       VALUES (%s,%s,%s,%s) """
   cursor = connection.cursor()
   result = cursor.executemany(sql_insert_query, a_list)
   connection.commit()
   print(cursor.rowcount, "Record inserted successfully into python_users table")
except pymysql.InternalError as error:
   code, message = error.args
   logfile.write(code, message)


logfile.close()
