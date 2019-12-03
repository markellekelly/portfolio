import os, sys, random, requests
from bs4 import BeautifulSoup
from nameparser import HumanName
import pymysql.cursors
import os

def spacing(s):
    if len(s.replace(" ","")) == 0:
        return(None)
    else:
        left = 0
        while s[left] == " ":
            left += 1
        if s[-1] == " ":
            right = -1
            while s[right] == " ":
                right -= 1
            return(s[left:right+1])
        return(s[left:])
        

def main():
    logfile = open('sustainerlog.txt','a')
    connection = pymysql.connect(host='localhost',
                            user='jmabel466',
                            password='****',
                            db='jmabel466',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    url = "https://csc.calpoly.edu/faculty/"
    
    try:
        myRequest = requests.get(url, verify=False)

        soup = BeautifulSoup(myRequest.text,"html.parser")

        tables = soup.find_all('table')
        faculty = tables[0]
        active_emer = tables[2]
        lecturers = tables[3]

        facultyInfo = faculty.find_all('tr')[1:]

        faculty_names = []
        faculty_positions = []
        faculty_emails = []
        faculty_offices = []

        for i in facultyInfo:
            info = i.find_all('td')
            names = info[0].text.split("\n")[0].replace("\n", "")[:-1]
            positions = info[0].text.split("\n")[1:]
            positions = list(filter(None, [spacing(x.replace("-", "")) for x in positions]))
            emails = info[1].text.replace("(place an 'at' sign here)", '@')
            offices = info[2].text

            faculty_names.append(names)
            faculty_positions.append(positions)
            faculty_emails.append(emails)
            faculty_offices.append(offices)
        

        chair = []
        faculty_positions2 = []
        for f in faculty_positions:
            if len(f) > 1:
                chair.append(1)
                faculty_positions2.append(f[1])
            else:
                chair.append(0)
                faculty_positions2.append(f[0])

            
        for i in range(len(faculty_names)):
            name = HumanName(faculty_names[i])
            statement = "INSERT INTO facultyInfo (FirstName, LastName, Position, Chair, Email, Office) VALUES ("
            statement += ('"' + name.first + '"' + ", " +
                            '"' + name.last + '"' + ", "  
                            + '"'+ faculty_positions2[i] + '"' + ", "
                            +  str(chair[i])  + ", "
                            + '"' + faculty_emails[i] + '"' + ", "
                            + '"' + faculty_offices[i] + '"' + ");\n")
            try:
                with connection.cursor() as cursor:
                    cursor.execute(statement)
                connection.commit()
            except:
                logfile.write("Could not insert faculty info statement " + str(i))

        emeritiInfo = active_emer.find_all('tr')[1:]

        active_emer_names = []
        active_emer_positions = []
        active_emer_emails = []
        active_emer_offices = []

        for i in emeritiInfo:
            info = i.find_all('td')
            names = info[0].text.split("\n")[0].replace("\n", "")[:-1]
            positions = info[0].text.split("\n")[1:]
            positions = list(filter(None, [spacing(x.replace("-", "")) for x in positions]))
            emails = info[1].text.replace("(place an 'at' sign here)", '@')
            offices = info[2].text

            active_emer_names.append(names)
            active_emer_positions.append(positions)
            active_emer_emails.append(emails)
            active_emer_offices.append(offices)
        #print(active_emer_names)
        #print(active_emer_positions)
        # print(active_emer_emails)
        # print(active_emer_offices)

        echair = []
        faculty_emer_positions = []
        for f in active_emer_positions:
            if len(f) > 1:
                echair.append(1)
                faculty_emer_positions.append(f[1])
            else:
                echair.append(0)
                faculty_emer_positions.append(f[0])

        for i in range(len(active_emer_names)):
            name = HumanName(faculty_names[i])
            statement = "INSERT INTO EmeritiInfo (FirstName, LastName, Position, Chair, Email, Office) VALUES ("
            statement += ('"' + name.first + '"' + ", " +
                            '"' + name.last + '"' + ", "  
                            + '"'+ faculty_emer_positions[i] + '"' + ", "
                            +  str(echair[i])  + ", "
                            + '"' + active_emer_emails[i] + '"' + ", "
                            + '"' + active_emer_offices[i] + '"' + ");\n")
            try:
                with connection.cursor() as cursor:
                    cursor.execute(statement)
                connection.commit()
            except:
                logfile.write("Could not insert emeriti info statement " + str(i))

        emeritiInfo = lecturers.find_all('tr')[1:]

        l_names = []
        l_emails = []
        l_offices = []

        for i in emeritiInfo:
            info = i.find_all('td')
            names = info[0].text.replace("\n", "")
            emails = info[1].text.replace("(place an 'at' sign here)", '@')
            offices = info[2].text

            l_names.append(names)
            l_emails.append(emails)
            l_offices.append(offices)

        for i in range(len(l_names)):
            name = HumanName(faculty_names[i])
            statement = "INSERT INTO Lecturers (FirstName, LastName, Email, Office) VALUES ("
            statement += ('"' + name.first + '"' + ", " +
                            '"' + name.last + '"' + ", " 
                            + '"' + l_emails[i] + '"' + ", "
                            + '"' + l_offices[i] + '"' + ");\n")

            try:
                with connection.cursor() as cursor:
                    cursor.execute(statement)
                connection.commit()
            except:
                logfile.write("Could not insert lecturers info statement " + str(i))

        all_names = []
        for n1 in faculty_names:
            if n1 not in all_names:
                all_names.append(n1)
        for n2 in active_emer_names:
            if n2 not in all_names:
                all_names.append(n2)
        for n3 in l_names:
            if n3 not in all_names:
                all_names.append(n3)

        counter = 1
        for i in all_names:
            name = HumanName(i)
            statement = "INSERT INTO Names (FirstName, LastName, ID) VALUES (" 
            statement += ('"' + name.first + '"' + ", " +
                            '"' + name.last + '"' + ", " +
                            str(counter) + ');\n')
            counter += 1
            try:
                with connection.cursor() as cursor:
                    cursor.execute(statement)
                connection.commit()
            except:
                logfile.write("Could not insert name info statement " + i)
    except:
        logfile.write('Whoops')
    logfile.close()

if __name__ == "__main__":
    main()
