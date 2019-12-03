import os, sys, random, requests
from bs4 import BeautifulSoup
from nameparser import HumanName
import re
from requests.exceptions import ConnectionError
import pymysql
from collections import Counter

logfile = open('sustainerlog.txt','a')
a_list = []
url = "https://github.com/jbclements/CSC-department-history/wiki/Faculty-&-Staff-Names"
myRequest = requests.get(url, verify=False)

soup = BeautifulSoup(myRequest.text,"html.parser")

professorsites = []
lists = soup.find_all('ul')
professorrecords = []
for item in lists[12].find_all('li'):
   breakdown = item.text.split(',')
   startandfinal = breakdown[1].replace('(','').replace(')','').split('-')
   if len(startandfinal) > 1:
      if startandfinal[1] == '?':
         startandfinal[1] = 'NULL'
      if '?' in startandfinal[1]:
         startandfinal[1] = startandfinal[1].replace('?','')
      if startandfinal[1] == '':
         startandfinal[1] = '2019'
   else:
      startandfinal.append('NULL')
   startandfinal.append(HumanName(breakdown[0]).first.lstrip().strip())
   startandfinal.append(HumanName(breakdown[0]).last.lstrip().strip())
   startandfinal.append(breakdown[-1].lstrip().strip())
   professorrecords.append(startandfinal)

try:
   connection = pymysql.connect(
     host="localhost",
     user="jmabel466",
     passwd="****",
     database="jmabel466"
   )

   sql_insert_query = """INSERT INTO tenureinformation (startdate, enddate, FirstName, LastName, almamater)
                       VALUES (%s,%s, %s, %s, %s) """
   cursor = connection.cursor()
   result = cursor.executemany(sql_insert_query, professorrecords)
   connection.commit()
except pymysql.InternalError as error:
   code, message = error.args
   logfile.write(code, message)

logfile.close()
