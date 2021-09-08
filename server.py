from bottle import request, run, post, route
import DBfunctions as dbf

import city_lis
city_list = city_lis.city_list


'''
server.py: handles all of the client HTTP requests

this file can be run in terminal using command:
    python server.py

can be accessed through routes:
    http://localhost:8080/weather
    http://localhost:8080/weather/<state>/<city>

also in http://localhost:8501, there is a checkbox which activates a POST request option
'''

@route("/weather")
def weather():
    '''
    return json object of DB entries
    '''
    conn = dbf.create_connection('data/weather.db')
    sql = 'SELECT * FROM weather'
    cur = conn.cursor()
    data = cur.execute(sql)
    temp = dict()
    # data is state, city, temp
    count = 0
    for row in data:
        temp[str(count)] = row
        count += 1
    conn.close()
    return temp
    

@post('/weather/<state>/<city_name>')
# add city that the job will scrape
def addJob(state, city_name):
    '''
    add a city that the job will scrape
    '''
    try:
        param = request.json.get('params') 
    except:
        param = (state, city_name)
    
    results = dbf.update_single(param) # adds the entry to the DB for display
    if(results):
        city_lis.city_list.insert(0, param) # NOTE this line doesn't work ??
        return 'Added {}, {} to the job'.format(param[1], param[0].upper())
    else:
        return '404 - the requested city could not be found'


@route('/weather/<state>/<city_name>')
#  get the last temperature of the city
def temp(state, city_name):
    results = dbf.scrape(dbf.clean_input([(state,city_name)]))
    if(results):
        return {"state": results[0][0], "city": results[0][1], "temp": results[0][2]}
    else:
        return '404 - the requested page could not be found'


run(host="localhost", port=8080, reloader=True, debug=True)
#  change host to match line 104 in app.py for post to work. can also change to 10.0.0.200 to get network URL working
