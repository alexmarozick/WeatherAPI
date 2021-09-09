from genericpath import isfile
import posixpath
import sqlite3
import DBfunctions as dbf
import os.path
import city_lis

city_list = city_lis.city_list

'''
updateDB.py

This file is called by a Scheduler Task to run every 5 minutes
and to update the weather.db stored in the data/

This file will check if the DB exists. If it doesn't it will create the DB.
If it already exists, the script will delete all rows and fill using the city_list.
The number of entries inserted is capped by the global variable defined in DBfunctions.

'''


def update():
    # need to update DB with new results
    print("updating DB..")

    # fill weatherTemp with info by scraping from website    
    results = dbf.scrape(dbf.clean_input(city_list))
    filepath = "C:\\Users\\Alex\\OneDrive\\Desktop\\WeatherAPI\\data\\weather.db"

    #checking if file exists
    if(os.path.exists(filepath)):
        # db exists
        print("deleting database rows..")
        # conn = dbf.create_connection('data/weather.db')
        conn = sqlite3.connect(filepath)
        cur = conn.cursor()
        dbf.delete_all_weather(conn)  #delete all rows

    else:
        # db doesnt exist
        print("creating database..")
        # conn = dbf.create_connection('data/weather.db')
        conn = sqlite3.connect(filepath)
        cur = conn.cursor()
        cur.execute('''
                    CREATE TABLE weather (State TEXT, City TEXT, Temperature INTEGER)
                    ''')
    
    # fill weather rows
    print("filling database rows...")
    sqlite_insert = '''
                    INSERT INTO weather
                    (State, City, Temperature)
                    VALUES (?, ?, ?)'''
    for loc in results:
        data = (loc[0], loc[1], loc[2])
        cur.execute(sqlite_insert, data)
    conn.commit()
    conn.close()
    print("DB connection closed")
    print("Update Complete")

update()