import os, sys, random, requests
from bs4 import BeautifulSoup
from collections import Counter
import unicodedata
from nameparser import HumanName
import pymysql

logfile = open('sustainerlog.txt','a')
url = "http://polyratings.com/list.php"
myRequest = requests.get(url)
page_names = set()

soup = BeautifulSoup(myRequest.text,"html.parser")
count = 0
for eventRow in soup.find_all('a',attrs={'class':'no-link-highlight text-muted filterable'}):
   for a_string in eventRow.strings:
      if 'CSC' in a_string:
         print(a_string)
         print(eventRow['href'])
         page_names.add(eventRow['href'])
         count += 1
print(page_names)

polydict = dict()
ratingslists = []
for name in page_names:
   url = name
   myRequest = requests.get(url)
   soup = BeautifulSoup(myRequest.text,"html.parser")
   for eventRow in soup.find_all('h1', attrs={'class': 'text-primary'}):
      teachername = ''.join(reversed(eventRow.text.split(', '))).replace('  ',' ')
      teachername = teachername.replace(u'\xa0\xa0', u' ')
      teachername = ''.join(c for c in unicodedata.normalize('NFKD', teachername) if unicodedata.category(c) != 'Mn')
      polydict[teachername] = dict()
   count = 0
   for eventRow in soup.find_all('span', attrs={'class': 'pull-right'}):
      for strings in eventRow.strings:
         if '/' in strings:
            polydict[teachername]['rating'] = strings.split('/')[0]
         if 'evaluations' in strings:
            polydict[teachername]['evaluations'] = strings.split(' ')[0]
         if 'Recognizes Student Difficulties:' in strings:
            polydict[teachername]['rsd'] = strings.split('Recognizes Student Difficulties: ')[1]
         if 'Presents Material Clearly:' in strings:
            polydict[teachername]['pmc'] = strings.split('Presents Material Clearly: ')[1]
   for item in ('rating','evaluations','rsd','pmc'):
      if item not in polydict[teachername]:
         polydict[teachername][item] = 0
   output = list()
   output.append(HumanName(teachername).first)
   output.append(HumanName(teachername).last)
   output.append(polydict[teachername]['rating'])
   output.append(polydict[teachername]['evaluations'])
   output.append(polydict[teachername]['rsd'])
   output.append(polydict[teachername]['pmc'])
   ratingslists.append(output)

for item in ratingslists:
   print(item)

try:
   connection = pymysql.connect(
     host="localhost",
     user="jmabel466",
     passwd="****",
     database="jmabel466",
     charset="utf8mb4"
   )
   sql_insert_query = """INSERT INTO ratings (FirstName, LastName, polyrating, numratings, seesdifficulty, presentsclearly) 
                       VALUES (%s,%s,%s,%s,%s,%s) """
   cursor = connection.cursor()
   result = cursor.executemany(sql_insert_query, ratingslists)
   connection.commit()
   print(cursor.rowcount, "Record inserted successfully into python_users table")
except pymysql.InternalError as error:
   code, message = error.args
   logfile.write(code, message)
logfile.close()
