import pymysql.cursors
import os

def main():
    connection1 = pymysql.connect(host='localhost',
                            user='nphillib466',
                            password='nphillibdb466',
                            db='nphillib466',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    statement = 'SELECT CONCAT(department," ", number) AS Courses, name AS CourseName FROM course;'
    course = []
    coursename = []
    try:
        with connection1.cursor() as cursor:
            cursor.execute(statement)
            result = cursor.fetchall()
            for i in result:
                course.append(i["Courses"].decode('UTF-8'))
                coursename.append(i["CourseName"])
        connection1.commit()
    except:
        print("Could not construct questions table.")
    finally:
        connection1.close()


    connection = pymysql.connect(host='localhost',
                            user='jmabel466',
                            password='****',
                            db='jmabel466',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    statement1 = "ALTER TABLE courses ADD COLUMN courseName VARCHAR(100);"
    try:
        with connection.cursor() as cursor:
            cursor.execute(statement1)
        connection.commit()
    except:
        print("Unable to add column courseName")

    for i in range(len(course)):
        up = ("UPDATE courses SET courseName = " + repr(coursename[i]).replace(".",'') + 
            " WHERE Courses = " + repr(course[i]) + ";")
        print(up)
        try:
            with connection.cursor() as cursor:
                cursor.execute(up)
            connection.commit()
        except:
            print("Unable to add the course name")

if __name__ == "__main__":
    main()
