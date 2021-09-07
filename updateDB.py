from genericpath import isfile
import DBfunctions as dbf
from os.path import isfile
import city_lis

city_list = city_lis.city_list

def update():
    # need to update DB with new results
    print("updating DB..")

    # fill weatherTemp with info by scraping from website    
    results = dbf.scrape(dbf.clean_input(city_list))
    
    
    #checking if file exists
    if(isfile('data/weather.db')):
        # db exists
        ("deleting database rows..")
        conn = dbf.create_connection('data/weather.db')
        cur = conn.cursor()
        dbf.delete_all_weather(conn)  #delete all rows

    else:
        # db doesnt exist
        print("creating database..")
        conn = dbf.create_connection('data/weather.db')
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