import os, sys, random, requests
from bs4 import BeautifulSoup
from nameparser import HumanName
import re
import mysql.connector
from requests.exceptions import ConnectionError

from collections import Counter

logfile = open('sustainerlog.txt','a')
a_list = []
url = "https://csc.calpoly.edu/faculty/"
myRequest = requests.get(url, verify=False)

soup = BeautifulSoup(myRequest.text,"html.parser")

professorsites = []
for eventRow in soup.find_all('td',attrs={'class':'namecell'}):
   for item in eventRow.find_all('a'):
      professorsites.append(item['href'])


contact_info = []
research_interests = []

for address in professorsites:
   contact_dict = dict()
   url = "https://csc.calpoly.edu" + address
   myRequest = requests.get(url, verify=False)
   soup = BeautifulSoup(myRequest.text,"html.parser")
   name = ''
   position = ''
   chair = 0

   for eventRow in soup.find_all('div', attrs={'id': 'mainLeftFull'}):
      for item in eventRow.find_all('h1'):
         name = HumanName(item.text)

   for eventRow in soup.find_all('div', attrs={'id': 'faculty-info'}):
      for item in eventRow.find_all('h3'):
         position = item.text.strip()
         if "Department Chair" in position:
            chair = 1
            position = position.replace('Department Chair','').lstrip()

   for eventRow in soup.find_all('div', attrs={'id': 'facultyContact'}):
      for item in eventRow.prettify().split('<br/>'):
         
         if 'Email:' in item.strip():
            for something in BeautifulSoup(item).find_all('a'):
               contact_dict['email'] = something.text.strip().replace('(place an \'at\' sign here)','@')
         if 'Office:' in item.strip():
            contact_dict['office'] = item.split('</strong>')[1].strip()
         if 'Phone Number:' in item.strip():
            contact_dict['phonenumber'] = item.split('</strong>')[1].strip()
         if 'Homepage:' in item.strip():
            for something in BeautifulSoup(item).find_all('a'):
               contact_dict['homepage'] = something.text.strip()
   for item in ('office', 'phonenumber', 'homepage', 'email'):
      if item not in contact_dict:
         contact_dict[item] = ''
   c_i_list = [name.first, name.last, position, chair, contact_dict['office'],contact_dict['phonenumber'],contact_dict['homepage'],contact_dict['email']]
   contact_info.append(c_i_list)

   for eventRow in soup.find_all('div', attrs={'class': 'facultyBlock'}):
      for aspan in eventRow.find_all('span'):
         print(aspan)

         aspan = aspan.prettify()
         aspan = aspan.replace('<span>','')
         aspan = aspan.replace('</span>','')
         for item in aspan.split('<br/>'):
            if len(item.strip()) > 0:
               name_and_interests = [name.first, name.last,item.strip()]
               research_interests.append(name_and_interests)
print(research_interests)
print(contact_info)

try:
   connection = pymysql.connect(
     host="localhost",
     user="jmabel466",
     passwd="****",
     database="jmabel466",
     charset='utf8mb4'
   )

   sql_insert_query = """INSERT INTO researchinterests (FirstName, LastName, researchinterests)
                       VALUES (%s,%s,%s) """
   cursor = connection.cursor()
   result = cursor.executemany(sql_insert_query, research_interests)
   connection.commit()
   print(cursor.rowcount, "Record inserted successfully into python_users table")

   sql_insert_query = """INSERT INTO instructors (FirstName, LastName, position, chair, room, phone, url, email)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """
   cursor = connection.cursor()
   result = cursor.executemany(sql_insert_query, contact_info)
   connection.commit()
   print(cursor.rowcount, "Record inserted successfully into python_users table")
except pymysql.InternalError as error:
   code, message = error.args
   logfile.write(code, message)
logfile.close()
