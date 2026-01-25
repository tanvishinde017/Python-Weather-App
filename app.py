from flask import Flask, render_template, request
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = error = None

    if request.method == "POST":
        city = request.form["city"].strip()

        if not city:
            error = "Enter a city name"
        else:
            res = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "units": "metric", "appid": API_KEY}
            ).json()

            if str(res.get("cod")) == "200":
                weather = {
                    "city": city.title(),
                    "temp": res["main"]["temp"],
                    "desc": res["weather"][0]["description"].title(),
                    "icon": res["weather"][0]["icon"]
                }
            else:
                error = res.get("message", "City not found")

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
