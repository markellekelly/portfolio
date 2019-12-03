import pymysql.cursors
import os

def main():
    connection = pymysql.connect(host='localhost',
                             user='jmabel466',
                             password='****',
                             db='jmabel466',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute(drop)
        connection.commit()
    except:
        print("Could not drop questions table.")

    table = ("CREATE TABLE questions(" +
    "team_id CHAR(2) NOT NULL," +
    "question VARCHAR(500) NOT NULL," +
    "answer VARCHAR(500)" +
    ");")

    try:
        with connection.cursor() as cursor:
            cursor.execute(table)
        connection.commit()
    except:
        print("Could not construct questions table.")

    f = "CSFacultyQs.txt"
    fin = open(f, 'r')
    for i in fin:
        info = i.split("|")
        statement = "INSERT INTO questions (team_id, question, answer) VALUES (" + repr(info[0]) + "," + info[1] + "," + info[2] +");"
        try:
            with connection.cursor() as cursor:
                cursor.execute(statement)
            connection.commit()
        except:
            print("Could not insert question into questions table ")
if __name__ == "__main__":
    main()
