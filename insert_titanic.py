import psycopg2
import sqlite3
import pandas as pd

dbname = 'eaelqpir'
user = 'eaelqpir'
password = 'F4xm5ehwEc3DI8UxR--OHCOJNA83mTyR'
host = 'chunee.db.elephantsql.com'

conn = psycopg2.connect(dbname=dbname, user=user,
                           password=password, host=host)
conn
curs = conn.cursor()

t_conn = sqlite3.connect('titanic.sqlite3')

df = pd.read_csv('titanic.csv')
df['Name'] = df['Name'].str.replace("'", "")
df.to_sql('titanic', con=t_conn, if_exists='replace')

t_curs = t_conn.cursor()
titanic = t_curs.execute('SELECT * FROM titanic;').fetchall()

create_titanic_table = """
    CREATE TABLE titanic_upload (
        index SERIAL PRIMARY KEY,
        Survived INT,
        Pclass INT,
        Name TEXT,
        Sex TEXT,
        Age REAL,
        Siblings_Spouses_Aboard INT,
        Parents_Children_Aboard INT,
        Fare FLOAT
    );
"""
curs.execute(create_titanic_table)
for passenger in titanic:
    insert_passenger = """
        INSERT INTO titanic_upload
        (Survived, Pclass, Name, Sex, Age, Siblings_Spouses_Aboard, 
        Parents_Children_Aboard, Fare)
        VALUES """ + str(passenger[1:]) + ';'
    curs.execute(insert_passenger)

curs.close()
conn.commit()