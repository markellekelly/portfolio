import os, sys, random, requests
from bs4 import BeautifulSoup
import pymysql.cursors
import os

def main():
    logfile = open('sustainerlog.txt','a')
    connection = pymysql.connect(host='localhost',
                            user='jmabel466',
                            password='****',
                            db='jmabel466',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    url_curr = "http://schedules.calpoly.edu/depts_52-CENG_curr.htm"
    try:
        # Current quarter
        myRequest = requests.get(url_curr)
        soup = BeautifulSoup(myRequest.text,"html.parser")
        quarter = soup.find("div", {"id":"infoblock1"}).find_all("span")[3].text
        rows = soup.find('table').find_all("tr")
        bind = 0
        for i in rows:
            if i.text.replace("\n","") == "CENG-Computer Science":
                break
            bind+=1     
        eind = 0
        for i in rows:
            splittext = i.text.split("\n")
            if eind > bind and eind != bind + 1 and splittext[1] == "Name":
                break
            eind+=1
        eind = eind - 1

        wantedinfo = rows[bind+2:eind]
        names = []
        ind = 0
        for i in wantedinfo:
            name = i.find("td", {"class":"personName"})
            if name != None:
                names.append(name.text)
        curr_firstnames = []
        curr_lastnames = []
        for n in names:
            splitter = n.split(",")
            l = splitter[0]
            f = splitter[1].split(" ")[1]
            curr_firstnames.append(f)
            curr_lastnames.append(l)

        curr_courses = []
        curr_sections = []
        curr_types = []
        curr_days = []
        curr_starts = []
        curr_ends = []
        curr_locations = []
        # Had to deal with the fact that the courses and other info were grouped together in a list
        # for each professor and were also singletons in a len(grouped list) lists 
        i = 0
        while i < len(wantedinfo):
            courses = []
            sections = []
            types = []
            days = []
            starts = []
            ends = []
            locations = []
            num = len(wantedinfo[i].find_all("td", {"class":"courseName active"}))
            for j in wantedinfo[i].find_all("td", {"class":"courseName active"}):
                courses.append(j.text)
            for j in wantedinfo[i].find_all("td", {"class":"courseSection active"}):
                sections.append(j.text.replace("\xa0",""))
            for j in wantedinfo[i].find_all("td", {"class":"courseType"}):
                types.append(j.text)
            for j in wantedinfo[i].find_all("td", {"class":"courseDays"}):
                days.append(j.text.replace("\xa0", "NULL"))
            for j in wantedinfo[i].find_all("td", {"class":"startTime"}):
                starts.append(j.text.replace("\xa0", "NULL"))
            for j in wantedinfo[i].find_all("td", {"class":"endTime"}):
                ends.append(j.text.replace("\xa0", "NULL"))
            for j in wantedinfo[i].find_all("td", {"class":"location"}):
                locations.append(j.text.replace("\xa0", "NULL"))
            if num > 0:
                i += num
            else:
                i += 1

            curr_courses.append(courses)
            curr_sections.append(sections)
            curr_types.append(types)
            curr_days.append(days)
            curr_starts.append(starts)
            curr_ends.append(ends)
            curr_locations.append(locations)

        qName = quarter[0:-13]
        year = quarter[-4:]

        currents = []
        for n in range(len(names)):
            p = (curr_firstnames[n], curr_lastnames[n], curr_courses[n],curr_sections[n], curr_types[n], curr_days[n], curr_starts[n],
                curr_ends[n], curr_locations[n])
            currents.append(p)

        clearer = "DELETE FROM Schedule;\n"

        try:
            with connection.cursor() as cursor:
                cursor.execute(clearer)
            connection.commit()
        except pymysql.InternalError as error:
            code, message = error.args
            logfile.write(code, message)

        for i in currents:
            for j in range(len(i[2])):
                statement = "INSERT INTO Schedule (FirstName, LastName, Courses, Sections, `Types`, `Days`, StartTime, EndTime, Locations, Quarter, `Year`) VALUES ("

                statement += ('"' + i[0] + '", ' +
                            '"' + i[1] + '", ' +
                            '"' + i[2][j] + '", ' +
                            '"' + i[3][j] + '", ' +
                            '"' + i[4][j] + '", ' +
                            '"' + i[5][j] + '", ' +
                            '"' + i[6][j] + '", ' +
                            '"' + i[7][j] + '", ' +
                            '"' + i[8][j] + '", ' +
                            '"' + qName + '", ' +
                            '"' + year + '");\n')
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(statement)
                    connection.commit()
                except:
                    logfile.write("Could not insert Schedule info statement " + i[0] + " " + i[1] + " " + qName)
        
    except:
        logfile.write("ERROR: Unable to open " + url_curr + "\n")

    # Last quarter
    url_last = "http://schedules.calpoly.edu/depts_52-CENG_last.htm"
    try:
        myRequest = requests.get(url_last)
        soup = BeautifulSoup(myRequest.text,"html.parser")

        quarter = soup.find("div", {"id":"infoblock1"}).find_all("span")[3].text
        rows = soup.find('table').find_all("tr")

        bind = 0
        for i in rows:
            if i.text.replace("\n","") == "CENG-Computer Science":
                break
            bind+=1
        
        eind = 0
        for i in rows:
            splittext = i.text.split("\n")
            if eind > bind and eind != bind + 1 and splittext[1] == "Name":
                break
            eind+=1
        eind = eind - 1

        wantedinfo = rows[bind+2:eind]
        names = []
        ind = 0
        for i in wantedinfo:
            name = i.find("td", {"class":"personName"})
            if name != None:
                names.append(name.text)
        last_firstnames = []
        last_lastnames = []
        for n in names:
            splitter = n.split(",")
            l = splitter[0]
            f = splitter[1].split(" ")[1]
            last_firstnames.append(f)
            last_lastnames.append(l)

        last_courses = []
        last_sections = []
        last_types = []
        last_days = []
        last_starts = []
        last_ends = []
        last_locations = []
        # Had to deal with the fact that the courses and other info were grouped together in a list
        # for each professor and were also singletons in a len(grouped list) lists 
        i = 0
        while i < len(wantedinfo):
            courses = []
            sections = []
            types = []
            days = []
            starts = []
            ends = []
            locations = []
            num = len(wantedinfo[i].find_all("td", {"class":"courseName active"}))
            for j in wantedinfo[i].find_all("td", {"class":"courseName active"}):
                courses.append(j.text)
            for j in wantedinfo[i].find_all("td", {"class":"courseSection active"}):
                sections.append(j.text.replace("\xa0", ""))
            for j in wantedinfo[i].find_all("td", {"class":"courseType"}):
                types.append(j.text.replace("\xa0", "NULL"))
            for j in wantedinfo[i].find_all("td", {"class":"courseDays"}):
                days.append(j.text.replace("\xa0", "NULL"))
            for j in wantedinfo[i].find_all("td", {"class":"startTime"}):
                starts.append(j.text.replace("\xa0", "NULL"))
            for j in wantedinfo[i].find_all("td", {"class":"endTime"}):
                ends.append(j.text.replace("\xa0", "NULL"))
            for j in wantedinfo[i].find_all("td", {"class":"location"}):
                locations.append(j.text.replace("\xa0", "NULL"))
            if num > 0:
                i += num
            else:
                i += 1

            last_courses.append(courses)
            last_sections.append(sections)
            last_types.append(types)
            last_days.append(days)
            last_starts.append(starts)
            last_ends.append(ends)
            last_locations.append(locations)

        qName = quarter[0:-13]
        year = quarter[-4:]
        lasts = []
        for n in range(len(names)):
            p = (last_firstnames[n], last_lastnames[n], last_courses[n],last_sections[n], last_types[n], last_days[n], last_starts[n],
                last_ends[n], last_locations[n])
            lasts.append(p)

        for i in lasts:
            for j in range(len(i[2])):
                statement = "INSERT INTO Schedule (FirstName, LastName, Courses, Sections, `Types`, `Days`, StartTime, EndTime, Locations, Quarter, `Year`) VALUES ("
                statement += ('"' + i[0] + '", ' +
                            '"' + i[1] + '", ' +
                            '"' + i[2][j] + '", ' +
                            '"' + i[3][j] + '", ' +
                            '"' + i[4][j] + '", ' +
                            '"' + i[5][j] + '", ' +
                            '"' + i[6][j] + '", ' +
                            '"' + i[7][j] + '", ' +
                            '"' + i[8][j] + '", ' +
                            '"' + qName + '", ' +
                            '"' + year + '");\n')
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(statement)
                    connection.commit()
                except:
                    logfile.write("Could not insert Schedule info statement " + i[0] + " " + i[1] + " " + qName)

    except:
        logfile.write("ERROR: Unable to open " + url_last + "\n")

    try:
        url_next = "http://schedules.calpoly.edu/depts_52-CENG_next.htm"
        myRequest = requests.get(url_next)
        soup = BeautifulSoup(myRequest.text,"html.parser")

        quarter = soup.find("div", {"id":"infoblock1"}).find_all("span")[3].text
        rows = soup.find('table').find_all("tr")

        bind = 0
        for i in rows:
            if i.text.replace("\n","") == "CENG-Computer Science":
                break
            bind+=1
        
        eind = 0
        for i in rows:
            splittext = i.text.split("\n")
            if eind > bind and eind != bind + 1 and splittext[1] == "Name":
                break
            eind+=1
        eind = eind - 1

        wantedinfo = rows[bind+2:eind]
        names = []
        ind = 0
        for i in wantedinfo:
            name = i.find("td", {"class":"personName"})
            if name != None:
                names.append(name.text)

        next_firstnames = []
        next_lastnames = []
        for n in names:
            splitter = n.split(",")
            l = splitter[0]
            f = splitter[1].split(" ")[1]
            next_firstnames.append(f)
            next_lastnames.append(l)

        next_courses = []
        next_sections = []
        next_types = []
        next_days = []
        next_starts = []
        next_ends = []
        next_locations = []
        i = 0
        while i < len(wantedinfo):
            courses = []
            sections = []
            types = []
            days = []
            starts = []
            ends = []
            locations = []
            num = len(wantedinfo[i].find_all("td", {"class":"courseName active"}))
            for j in wantedinfo[i].find_all("td", {"class":"courseName active"}):
                courses.append(j.text)
            for j in wantedinfo[i].find_all("td", {"class":"courseSection active"}):
                sections.append(j.text.replace("\xa0", ""))
            for j in wantedinfo[i].find_all("td", {"class":"courseType"}):
                types.append(j.text.replace("\xa0", "NULL"))
            for j in wantedinfo[i].find_all("td", {"class":"courseDays"}):
                days.append(j.text.replace("\xa0", "NULL"))
            for j in wantedinfo[i].find_all("td", {"class":"startTime"}):
                x = j.text.replace("\xa0", "NULL")
                starts.append(x)
            for j in wantedinfo[i].find_all("td", {"class":"endTime"}):
                x = j.text.replace("\xa0", "NULL")
                ends.append(x)
            for j in wantedinfo[i].find_all("td", {"class":"location"}):
                locations.append(j.text.replace("\xa0", "NULL"))
            if num > 0:
                i += num
            else:
                i += 1
            next_courses.append(courses)
            next_sections.append(sections)
            next_types.append(types)
            next_days.append(days)
            next_starts.append(starts)
            next_ends.append(ends)
            next_locations.append(locations)


        qName = quarter[0:-13]
        year = quarter[-4:]
        nexts = []
        for n in range(len(names)):
            p = (next_firstnames[n],next_lastnames[n], next_courses[n],next_sections[n], next_types[n], next_days[n], next_starts[n],
                next_ends[n], next_locations[n])
            nexts.append(p)

        for i in nexts:
            for j in range(len(i[2])):
                statement = "INSERT INTO Schedule (FirstName, LastName, Courses, Sections, `Types`, `Days`, StartTime, EndTime, Locations, Quarter, `Year`) VALUES ("
                statement += ('"' + i[0] + '", ' +
                            '"' + i[1] + '", ' +
                            '"' + i[2][j] + '", ' +
                            '"' + i[3][j] + '", ' +
                            '"' + i[4][j] + '", ' +
                            '"' + i[5][j] + '", ' +
                            '"' + i[6][j] + '", ' +
                            '"' + i[7][j] + '", ' +
                            '"' + i[8][j] + '", ' +
                            '"' + qName + '", ' +
                            '"' + year + '");\n')
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(statement)
                    connection.commit()
                except:
                    logfile.write("Could not insert Schedule info statement " + i[0] + " " + i[1] + " " + qName)
    except:
        logfile.write("ERROR: Unable to open " + url_next + "\n")

    timestr = 'UPDATE Schedule SET StartTime = STR_TO_DATE(StartTime, "%l:%i %p");\n'
    try:
        with connection.cursor() as cursor:
            cursor.execute(timestr)
        connection.commit()
    except pymysql.InternalError as error:
        code, message = error.args
        logfile.write(code, message)
    timestr = 'UPDATE Schedule SET EndTime = STR_TO_DATE(EndTime, "%l:%i %p");'
    try:
        with connection.cursor() as cursor:
            cursor.execute(timestr)
        connection.commit()
    except pymysql.InternalError as error:
        code, message = error.args
        logfile.write(code, message)

    up = "update Schedule set Locations=RIGHT(Locations,length(Locations)-1) where Locations like '0%';"
    try:
        with connection.cursor() as cursor:
            cursor.execute(up)
        connection.commit()
        with connection.cursor() as cursor:
            cursor.execute(up)
        connection.commit()
    except:
        logfile.write("Could not update office location info.")

    up = "UPDATE Schedule Set Locations=REPLACE(Locations, '-0', '-');"
    try:
        with connection.cursor() as cursor:
            cursor.execute(up)
        connection.commit()
    except:
        logfile.write("Could not update office location info.")
    logfile.close()

if __name__ == "__main__":
    main()
