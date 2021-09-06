import app as a

def show_all_weather():
    '''
    Input: Connection to SQLite database
    Output: None

    Delete all rows in the weather table
    '''
    conn = a.create_connection('data/weather.db')
    sql = 'SELECT * FROM weather'
    cur = conn.cursor()
    data = cur.execute(sql)
    for row in data:
        print(row)
    conn.commit()
    conn.close()

show_all_weather()