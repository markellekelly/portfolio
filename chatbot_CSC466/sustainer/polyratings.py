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

sqllist = []
polydict = dict()
for name in page_names:
   url = name
   myRequest = requests.get(url)
   soup = BeautifulSoup(myRequest.text,"html.parser")
   for eventRow in soup.find_all('h1', attrs={'class': 'text-primary'}):
      teachername = ''.join(reversed(eventRow.text.split(', '))).replace('  ',' ')
      # print(''.join(reversed(eventRow.text.split(', '))).replace('  ',' '))
      teachername = teachername.replace(u'\xa0\xa0', u' ')
      teachername = ''.join(c for c in unicodedata.normalize('NFKD', teachername) if unicodedata.category(c) != 'Mn')
      polydict[teachername] = dict()     
   count = 0
   for sections in soup.find_all('section'):
      counts = Counter()
      classnum = ''
      for item in sections.find_all('h2'):
         classnum = item.text
      for item in sections.find_all('div', attrs={'class':"col-xs-3 col-sm-2 eval-info"}):
         count = 0
         for object in item.strings:
            if count == 1:
               counts.update(object.split())
            count += 1

      counts['Credit'] = 0
      counts['N/A'] = 0
      counts += Counter()
      countnum = sum(counts.values())
      counts['A'] = counts['A'] * .95
      counts['B'] = counts['B'] * .85
      counts['C'] = counts['C'] * .75
      counts['D'] = counts['D'] * .65
      counts['F'] = counts['F'] * .55
      counts['Withdrawn'] = counts['Withdrawn'] * .55
      counts += Counter()
      totalnum = sum(counts.values())
      if countnum > 0:
         atuple = (HumanName(teachername).first,HumanName(teachername).last,classnum,str(totalnum/countnum))
         sqllist.append(atuple)
      else:
         atuple = (HumanName(teachername).first,HumanName(teachername).last,classnum,str(0.00))
         sqllist.append(atuple)
print(sqllist)

try:
   connection = pymysql.connect(
     host="localhost",
     user="jmabel466",
     passwd="****",
     database="jmabel466",
     charset='utf8mb4'
   )

   sql_insert_query = """INSERT INTO courses (FirstName, LastName, Courses, averagegrade)
                       VALUES (%s,%s,%s,%s) """
   cursor = connection.cursor()
   result = cursor.executemany(sql_insert_query, sqllist)
   connection.commit()
   logfile.write(cursor.rowcount, "Record inserted successfully into python_users table")
except pymysql.InternalError as error:
   code, message = error.args
   logfile.write(code, message)
logfile.close()
