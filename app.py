# Core Pkgs
from pandas.io.sql import read_sql_query
import streamlit as st
import pandas as pd

# # DB Management
# import sqlite3
# from sqlite3 import Error
import time

from math import ceil
# import numpy as np

import DBfunctions as dbf




def display_full_database(conn):
    '''
    Pagination in streamlit has to be done manually.
    Page_size determines how many datapoints are viewed at once
    Page_number determines which page is visible
    '''
    query = "SELECT State, City, Temperature from weather"
    df = pd.read_sql_query(query,conn)

    page_size = 10
    page_number = st.number_input(
        label="Page Number",
        min_value=1,
        max_value=ceil(len(df)/page_size),
        step=1,
    )
    current_start = (page_number-1)*page_size
    current_end = page_number*page_size
    st.write(df[current_start:current_end])

def display_query_results(query, conn, param):
    '''
    Input: ((SQL query string), SQLite Connection Object)
    Output: None on fail

    This function will query for specific entries within the database and display results
    '''
    df = pd.read_sql_query(query, conn, params = param)
    if(not df.empty):
        st.success("Success!")
        st.write(df)
    else:
        if(len(param)==1):
            st.warning("No results found in Database")
        if(len(param) == 2):
            # update DB with city or report that city cant be found
            st.warning("Location not in database.. checking now")
            update_success = dbf.update_single(param)
            # time.sleep(2)
            #TODO Make it so that when you type
            print("update success: ",update_success)
            if(update_success):
                conn = dbf.create_connection("data/weather.db")
                return display_query_results(query, conn, param)
            else:
                st.error("City can't be found")

def main():

    st.title("Real-Time Temperature of US Cities")

    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")

        conn = dbf.create_connection("data/weather.db")
        display_full_database(conn)

        st.markdown("# Choose a Location!")
        input_city = (st.text_input("City Name", "Type Here...")).replace(' ','-').lower().strip()
        input_state = (st.text_input("Abbreviation of State", "Type Here...")).lower().strip()
        

        if(st.button('Submit')):
            if(input_city and not input_state):  # query for all city_name matches 
                param = (input_city,)
                sql_query = '''SELECT State, City, Temperature FROM weather WHERE City = ?'''
                display_query_results(sql_query, conn, param)

            elif(not input_city and input_state):   # query for all cities within a state
                param = (input_state,)
                sql_query = '''SELECT State, City, Temperature FROM weather WHERE State = ?'''
                display_query_results(sql_query, conn, param)

            elif(input_city and input_state):    # query for state, city pair
                param = (input_state, input_city)
                sql_query = '''SELECT State, City, Temperature FROM weather WHERE State = ? AND City = ?'''
                display_query_results(sql_query, conn, param)
            
            else:
                st.warning("Uh oh.. Fill one of the boxes first!")
            
                
    else:
        st.subheader("About")
        
        st.markdown("## Purpose of Webapp:")
        st.text("Originally, I created this project for a job application!\nThis project gave me exposure to all of the software described below!")


if __name__ == '__main__':
    main()

# streamlit run app.py