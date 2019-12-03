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


    drop = "DROP TABLE IF EXISTS facultyInfo;"
    try:
        with connection.cursor() as cursor:
            cursor.execute(drop)
        connection.commit()
    except:
        f.write("Could not drop facultyInfo table.")

    drop = "DROP TABLE IF EXISTS EmeritiInfo;"
    try:
        with connection.cursor() as cursor:
            cursor.execute(drop)
        connection.commit()
    except:
        f.write("Could not drop EmeritiInfo table.")

    drop = "DROP TABLE IF EXISTS Lecturers;"
    try:
        with connection.cursor() as cursor:
            cursor.execute(drop)
        connection.commit()
    except:
        f.write("Could not drop Lecturers table.")
    
    drop = "DROP TABLE IF EXISTS Names;"
    try:
        with connection.cursor() as cursor:
            cursor.execute(drop)
        connection.commit()
    except:
        f.write("Could not drop Names table.")

    table = ("CREATE TABLE facultyInfo(" +
    "FirstName VARCHAR(100) NOT NULL," +
    " LastName VARCHAR(100) NOT NULL," +
    "Position VARCHAR(100) NOT NULL," +
    "Chair INTEGER NOT NULL," +
    "Email VARCHAR(20) NOT NULL," +
    "Office VARCHAR(10) NOT NULL," +
    "PRIMARY KEY (FirstName, LastName)" +
    ");")

    try:
        with connection.cursor() as cursor:
            cursor.execute(table)
        connection.commit()
    except:
        f.write("Could not construct facultyInfo table.")

    table = ("CREATE TABLE EmeritiInfo(" +
    "FirstName VARCHAR(100) NOT NULL," +
    "LastName VARCHAR(100) NOT NULL," +
    "Position VARCHAR(100) NOT NULL," +
    "Chair INTEGER NOT NULL," +
    "Email VARCHAR(20) NOT NULL," +
    "Office VARCHAR(10) NOT NULL," +
    "PRIMARY KEY (FirstName, LastName)" +
    ");")

    try:
        with connection.cursor() as cursor:
            cursor.execute(table)
        connection.commit()
    except:
        f.write("Could not construct EmeritiInfo table.")

    table = ("CREATE TABLE Lecturers(" +
    "FirstName VARCHAR(100) NOT NULL," +
    "LastName VARCHAR(100) NOT NULL," +
    "Email VARCHAR(20) NOT NULL," +
    "Office VARCHAR(10) NOT NULL," +
    "PRIMARY KEY (FirstName, LastName)" +
    ");")

    try:
        with connection.cursor() as cursor:
            cursor.execute(table)
        connection.commit()
    except:
        f.write("Could not construct Lecturers table.")

    table = ("CREATE TABLE Names(" +
    "FirstName VARCHAR(100) NOT NULL," +
    "LastName VARCHAR(100) NOT NULL," +
    "ID INTEGER NOT NULL," +
    "PRIMARY KEY (ID)" +
    ");")

    try:
        with connection.cursor() as cursor:
            cursor.execute(table)
        connection.commit()
    except:
        f.write("Could not construct Names table.")
    f.close()

if __name__ == "__main__":
    main()
