# AWS Web application to find the geo-closest cities based on the input city

This is an web application/ service which allow the user to select any city name, region/state and country to find the closest cities. <br />
The user needs to provide the city and either the input for the number of cities cloestest or display the cities within the distance limit. <br />
This application normally takes <1 sec to respond by going through all the cities in the large dataset.

# Service provided:
1. Able to query and display the results in < 1 sec for limit 10 kms and 10 cities  <br />
2. Use Elastic Memcache to increase the speed for redudant queries <br />

# Technologies used:
1. AWS EC2 instance <br />
2. MySql Db instance <br />
3. Elastic Memcache <br />
4. Flask for web interface 
