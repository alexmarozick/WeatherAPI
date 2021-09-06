from genericpath import isfile
import app as a
import requests
from bs4 import BeautifulSoup
from os.path import isfile

def scrape(cities):
    '''
    Input: [("state","city-name")]
        restrictions: state must be lowercase and acronym, city-name must be lowercase and space replaced with -
                    ex.  ("ca", "san-jose")
    Output: [("state","city-name",temp)]

    This function takes in a list of cities and scrapes the temperature of each one using BeautifulSoup
    '''

    base_URL = "https://www.wunderground.com/weather/us/"
    results = []

    for loc in cities:
        state,city = loc
        URL = base_URL + "/"+ state + "/" + city

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        temp = soup.find("span", {'class':'wu-value wu-value-to'}).get_text()
        
        loc_and_temp = (state, city, int(temp))
        results.append(loc_and_temp)
    
    return results

def clean_input(locs):
    '''
    Input: [("state","city-name")]
    Output: [("state","city-name")]

    This function takes in a list of state/city tuples and cleans input so scraping is always correct, even if the user inputs the state/city.
    It lowercases and changes spaces to hyphens
    '''
    cleaned_input = []
    for loc in locs:
        state = loc[0].lower()
        city = loc[1].replace(' ','-').lower()
        cleaned_input.append((state, city))
    return cleaned_input

def delete_all_weather(conn):
    '''
    Input: Connection to SQLite database
    Output: None

    Delete all rows in the weather table
    '''
    sql = 'DELETE FROM weather'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()



def update():
    # need to update DB with new results
    print("updating DB..")

    cities = [("Ca","santa cruz"), ("ca","san Jose"), ("OR", "EugEnE"), ("or", "portland")]
    # fill weatherTemp with info by scraping from website    
    results = scrape(clean_input(cities))
    
    
    #checking if file exists
    if(isfile('data/weather.db')):
        # db exists
        ("deleting database rows..")
        conn = a.create_connection('data/weather.db')
        cur = conn.cursor()
        delete_all_weather(conn)  #delete all rows

    else:
        # db doesnt exist
        print("creating database..")
        conn = a.create_connection('data/weather.db')
        cur = conn.cursor()
        cur.execute('''
                    CREATE TABLE weather (id INTEGER PRIMARY KEY, state TEXT, city TEXT, temp INTEGER)
                    ''')
    
    # fill weather rows
    print("filling database rows...")
    id_num = 0
    sqlite_insert = '''
                    INSERT INTO weather
                    (id, state, city, temp)
                    VALUES (?, ?, ?, ?)'''
    for loc in results:
        id_num += 1
        data = (id_num, loc[0], loc[1], loc[2])
        cur.execute(sqlite_insert, data)
    conn.commit()
    conn.close()
    print("DB connection closed")
    print("Update Complete")

update()