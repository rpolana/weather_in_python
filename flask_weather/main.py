from flask import Flask, render_template, request, json
import requests
import geocoder
from pprint import pprint
import re
from datetime import date, timedelta, datetime

app = Flask(__name__)
url = 'https://api.darksky.net/forecast/038b181513c81f4834031aa14d5b45f3/'
#url = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/weather', methods=['POST'])
def weather():
    address = request.form['address']
    if 'openweathermap' in url:
        if re.match(r'^\s*\d{6}\s*$', address) == None:
            r = requests.get(url + '?q=' + address + ',in&appid=25b3bfd96d8f75c5df33f4fa26e59fbf')
        else:
            r = requests.get(url+'?zip='+address+',in&appid=25b3bfd96d8f75c5df33f4fa26e59fbf')
    elif 'darksky' in url:
        try:
            g = geocoder.google(address)
            if g.status_code != requests.codes.ok:
                return 'Error: Please enter valid zipcode or city name'
            if g.status == 'OVER_QUERY_LIMIT':
                return 'Error: Number of free queries exceeded, try after a few minutes'
            print str(g.current_result.lat)+','+str(g.current_result.lng)
            r = requests.get(url+
                str(g.current_result.lat)+','+str(g.current_result.lng)+'?exclude=minutely,hourly&units=si')
        except:
            return 'Error: Please enter valid zipcode or address, country'
    else:
        return app.response_class(response="No weather service set.", status=500)
    print r
    print r.headers
    print r.content
    if r.status_code != requests.codes.ok:
        return 'Error: Please enter valid zipcode or city name'
    json_object = r.json()
    print json_object
    # return app.response_class(
    #    response=json.dumps(r.text),
    #    status=200,
    #    mimetype='application/json'
    #)
    if 'openweathermap' in url:
        temp_k = float(json_object['main']['temp'])
        temp_c = "%.1f"%(temp_k - 273.15);
        temp_f = "%.1f"%((temp_k - 273.15) * 1.8 + 32);
        name = json_object['name']
        humidity = float(json_object['main']['humidity'])
        wind_speed = "%.2f" % (float(json_object['wind']['speed']) * 60.0 / 1000.0)
        print json_object
        return render_template('weather_openweathermap.html', temp_c=temp_c, temp_f=temp_f,
                               wind_speed=wind_speed, weather=json_object)
    elif 'darksky' in url:
        json_object['temp_c'] = "%.1f"%(json_object['currently']['temperature'])
        json_object['temp_f'] = "%.1f" % ((json_object['currently']['temperature']) * 1.8 + 32)
        json_object['name'] = str(g.current_result)
        json_object['humidity'] = "%.1f" % (float(json_object['currently']['humidity']) * 100.0)
        json_object['wind_speed'] = "%.2f" % (float(json_object['currently']['windSpeed']) * 3600.0 / 1000.0 )
        json_object['precipitation'] = "%3.0f" % (float(json_object['currently']['precipProbability']) * 100.0)
        weekday = date.today()
        json_object['current_time'] = date.strftime(datetime.now(), "%c")
        forecast = []
        forecast.append(dict(summary=json_object['daily']['summary']))
        n_days = 0
        for day in json_object['daily']['data']:
            n_days += 1
            forecast.append(dict(
                day=date.strftime(weekday, '%a %b %d'),
                summary=day['summary'],
                temperatureMin="%.1f" % day['temperatureMin'],
                temperatureMax="%.1f" % day['temperatureMax'],
                precipitation="%3.0f" % (day['precipProbability'] * 100),
            ))
            weekday += timedelta(days=1)
        return render_template('weather_darksky.html',
                               weather=json_object, forecast=forecast, n_days=n_days-1)
    else:
        return app.response_class(response="No weather service set.", status=500)

@app.route('/')
def index():
    if 'openweathermap' in url:
        label = 'Please enter zipcode or city in India'
    elif 'darksky' in url:
        label = 'Please enter location, country'
    else:
        return app.response_class(response="No weather service set.", status=500)
    return render_template('index.html', label=label)

if __name__== "__main__":
    app.run(debug=True)
