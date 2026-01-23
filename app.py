from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            error = "Please enter a city name"
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
            response = requests.get(url).json()

            if response.get("cod") != 200:
                error = "City not found"
            else:
                weather = {
                    "city": city.title(),
                    "temp": response["main"]["temp"],
                    "desc": response["weather"][0]["description"].title(),
                    "icon": response["weather"][0]["icon"]
                }

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
