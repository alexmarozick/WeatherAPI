# WeatherAPI   
REST API to display US weather data to users   

# Functionality:   
The API will provide a list of REST endpoints:   
  - GET /weather   list the cities (with pagination if possible)   
  - POST  /weather/city   to add a city that the job will scrape   
  - GET   /weather/city   to get the last temperature of the city, returning 404 if the city has not been added yet   

# Dependencies
All of them are listed in requirements.txt and is supposed to run on Windows machine.

# How to run
To run the frontend, type "streamlit run app.py" into the terminal
    url:
        http://localhost:8501


 To run the server that will handle HTTP requests, type "python server.py" into the terminal
    routes:
        http://localhost:8080/weather
        http://localhost:8080/weather/<state>/<city>




# Design/Implementation   
   
BeautifulSoup4:
    I chose to use beautifulsoup to scrape the temperatures off of the site https://www.wunderground.com/weather/us/. 

Database:  SQLite   
  The reason for choosing this database is that these databases are easy to implement, are suitable for the data I will be representing, and were be easy to make queries to display the data on the webpage. The data is composed of city names, the state they belong to, and the latest updated temperature.
  
Front-end: Streamlit   
  Streamlit turns data scripts into a shareable webapp efficiently. It is coded in python, requires no front end experience, and should run off the database smoothly.

Web Framework: Bottle
    Used bottle to process the HTTP requests from the user.

Cron Job: Schtasks
    Schtasks is the Windows equivalent to linux's cron jobs. I set a task to run the updateDB.py script every 5 minutes. This will keep the DB up to date with the current temperature every 5 minutes.


# Issues
1) Frontend and HTTP request handler run off different urls

2) Initializing DB with many entries is very slow due to scraping one at a time

3) Task scheduler doesnt update DB even though it calls the correct script
    For now, update DB by calling "python ./updateDB.py"
