import geocoder

g = geocoder.ip('me')
location = g.latlng
lat = location[0]
lon = location[1]


API_KEY = "06923fb22252c8af8f30c90a35b70f92"
URL ="http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric".format(lat, lon, API_KEY)
