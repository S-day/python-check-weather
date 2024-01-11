from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

#makes an app as a Flask app
app = Flask(__name__)

#After setting up the Flask app, you would typically define routes (URL patterns) and their corresponding view functions.
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


#Handle route from weather.py
@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    #check for empty strings or string with only spaces
    if not bool(city.strip()):
      city = "Wuhan" 

    weather_data = get_current_weather(city)

    #City is not found by API
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')

    #send the data from weather to template
    return render_template(
        "weather.html",
        title=weather_data["name"],
        #0 is to get the first element in weather
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"

    )

if __name__ == "__main__" :
    serve(app, host="0.0.0.0", port=8000)