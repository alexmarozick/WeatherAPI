# WeatherAPI
REST API to display US weather data to users

Functionality:
The API will provide a list of REST endpoints:
  - GET /weather   list the cities (with pagination if possible)
  - POST  /weather/city   to add a city that the job will scrape
  - GET   /weather/city   to get the last temperature of the city, returning 404 if the city has not been added yet


Design/Implementation

Weather API:
  Will be relying on this API for the data that will fill the SQLite database. There will be a chron job that makes a request for data every 5 minutes to this API and will then update the database with a new table.

Database:  SQLite
  The reason for choosing this database is that these databases are easy to implement, are suitable for the data I will be representing, and should be easy to make queries to display the data on the webpage. The data is composed of city names, the state they belong to, the latest updated temperature, and whether that is high/low.
  
Front-end: Streamlit
  Streamlit turns data scripts into a shareable webapp efficiently. It is coded in python, requires no front end experience, and should run off the database smoothly.

Hosting: Heroku
  Heroku is a cloud platform as a service (PaaS) that I have used before to host my web apps. 
