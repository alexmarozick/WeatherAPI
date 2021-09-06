# Core Pkgs
import streamlit as st

# DB Management
import sqlite3
from sqlite3 import Error

#c = conn.cursor()


def create_connection(database):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(database)
        print("establishing connection...")
        return conn
    except Error as e:
        print(e)
    # finally:
    #     if conn:
    #         conn.close()

def display_database(conn):
    print("displaying database...", conn)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE weather (id INTEGER PRIMARY KEY, city_name TEXT, state TEXT, temp INTEGER, general TEXT)''')

    #TODO display data every update
    #TODO pagination
    

    return None

#might need to set up chron job in a different file


def main():

    
    conn = create_connection()
    display_database(conn)   #TODO may want to move this inside homepage or something

    st.title("US Weather")

    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("HomePage")

        #TODO add tables for the home page
    
    else:
        st.subheader("About")

        #TODO talk about this project and the tech stack, chron jobs, DB choice, hosting
    

if __name__ == '__main__':
    main()

# streamlit run app.py



#chron job time */5 * * * * [command]