# Cafe-Wifi-API
I created this API based website to showcase my abilities in Python, RESTful API, HTML and Database.\
In it you can read directly on the website the current cafes and their info in the database.\
Everything else can be done via API as per below documentation:\
######
GET - Search Cafes By Location\
The /search route will return the Cafes around the location given, if any.\
Use the "loc" parameter to pass the location.\
######
GET - Get All Cafes\
Use the /all route to get a list of all the Cafes contained in database.\
#####
GET - Get Random Cafe\
Use the /random route to get a random Cafe contained in database.\
#####
POST - Post a New Cafe\
Use the /add route to add a new Cafe to database.\
name - name of the cafe\
map_url -  link to cafe's location\
img_url - an image of the cafe\
location - the address\
seats - number of seats available\
has_toilet - True/False, 0/1 or yes/no\
has_wifi - True/False, 0/1 or yes/no\
has_sockets - True/False, 0/1 or yes/no\
can_take_calls - True/False, 0/1 or yes/no\
coffee_price - coffee price





