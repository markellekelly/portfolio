import os, sys, random, requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from nameparser import HumanName
from collections import Counter
import pymysql

a_list = []
for i in range(1,261):
   url = "https://digitalcommons.calpoly.edu/csse_fac/" + str(i)
   try:
      myRequest = requests.get(url, verify=False)
      soup = BeautifulSoup(myRequest.text,"html.parser")

      for eventRow in soup.find_all('div',attrs={'id':'recommended_citation'}):
         for item in eventRow.find_all('p',attrs={'class':'comments'}):
            if item.find('em') is not None:
               for items in item.find('em'):
                   journal = items

      for eventRow in soup.find_all('p',attrs={'class':'author'}):
         for items in eventRow.find_all('strong'):
            name = HumanName(items.text)
            a_list.append((soup.head.title.get_text().split('by')[0].strip(),name.first,name.last,journal))
      print(a_list)

   except ConnectionError: 
      print('Whoops')

for item in a_list:
   print(item)

try:
   connection = pymysql.connect(
     host="localhost",
     user="jmabel466",
     passwd="****",
     database="jmabel466",
     charset='utf8mb4'
   )

   sql_insert_query = """INSERT INTO publications (papername, FirstName, LastName, journalname)
                       VALUES (%s,%s,%s,%s) """
   cursor = connection.cursor()
   result = cursor.executemany(sql_insert_query, a_list)
   connection.commit()
   print(cursor.rowcount, "Record inserted successfully into python_users table")
   connection.commit()
except pymysql.InternalError as error:
   code, message = error.args
   print(code, message)
