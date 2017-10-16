# weather_in_python
Integrate weather in web apps using python flask.

Run main.py starts a local webserver listening on port 5000.  Goto http://localhost:5000 to see the start page, where you can enter any city or zipcode or address in the world, and submit would take you to the current weather conditions and 7-day forecast for the input location.

Uses google geocode library to convert input location into latitude, longitude

Uses darksky.net weather api to pull weather data using latitude and longitude corresponding to the input.
