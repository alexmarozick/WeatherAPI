import requests
from bs4 import BeautifulSoup

from pandas.io.sql import read_sql_query
import pandas as pd

# DB Management
import sqlite3
from sqlite3 import Error

NUM_CITIES = 200   # NOTE this is the number of cities that will be in DB

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

    num = 0
    for loc in cities:
        print("num: ", num, "    loc: ", loc)
        num += 1
        if(num == NUM_CITIES):
            break
        state,city = loc
        URL = base_URL + "/"+ state + "/" + city

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        temp = soup.find("span", {'class':'wu-value wu-value-to'})
        if(temp == None):
            continue
        else:
            temp = temp.get_text()
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
        state = loc[0].lower().strip()
        city = loc[1].strip().replace(' ','-').lower()
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

def update_single(loc):
    '''
    Input: [("state","city-name")]
    Output: 1 on success, None on fail

    This function attempts to scrape temperature of user inputted city
    and either will return None on fail, or update DB and return 1 on success.
    '''
    conn = create_connection('data/weather.db')
    cur = conn.cursor()

    results = scrape(clean_input([loc]))

    if(results):
        sqlite_insert = '''
                        INSERT INTO weather
                        (State, City, Temperature)
                        VALUES (?, ?, ?)'''
        data = (results[0][0], results[0][1], results[0][2])
        cur.execute(sqlite_insert, data)
        conn.commit()
        conn.close()
        return 1
    else:
        conn.close()
        return None

def create_connection(database):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(database)
        print("establishing connection...")
        return conn
    except Error as e:
        print(e)

def get_data(conn):
    '''returns dataframe for all rows in weather DB'''
    df = pd.read_sql("SELECT * FROM weather", con=conn)
    return df