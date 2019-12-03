import pymysql.cursors
import os

def main():
    f = open('sustainerlog.txt','a')
    connection = pymysql.connect(host='localhost',
                            user='jmabel466',
                            password='****',
                            db='jmabel466',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)


    drop = "DROP TABLE IF EXISTS Schedule;"
    try:
        with connection.cursor() as cursor:
            cursor.execute(drop)
        connection.commit()
    except:
        f.write("Could not drop Schedule table.")

    table = ("CREATE TABLE Schedule(" +
    "FirstName VARCHAR(100) NOT NULL," +
    "LastName VARCHAR(100) NOT NULL," +
    "Courses VARCHAR(100)," +
    "Sections VARCHAR(20)," +
    "`Types` VARCHAR(10)," +
    "`Days` VARCHAR(10)," +
    "StartTime VARCHAR(10)," +
    "EndTime VARCHAR(10)," +
    "Locations VARCHAR(10)," +
    "Quarter VARCHAR(50) NOT NULL," +
    "`Year` VARCHAR(10) NOT NULL" +
    ");")

    try:
        with connection.cursor() as cursor:
            cursor.execute(table)
        connection.commit()
    except:
        f.write("Could not construct Schedule table.")
    f.close()

if __name__ == "__main__":
    main()
