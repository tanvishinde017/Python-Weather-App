from flask import Flask, render_template, request
import requests
import os
import redis
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Redis connection (Docker Compose service name = redis)
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        if not city:
            error = "Please enter a city name"
        else:
            # 🔹 Check cache
            cached_weather = redis_client.get(city)
            if cached_weather:
                return cached_weather

            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "units": "metric",
                "appid": API_KEY
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                weather = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"].title(),
                    "icon": data["weather"][0]["icon"]
                }

                rendered_page = render_template("index.html", weather=weather)

                # 🔹 Cache for 5 minutes
                redis_client.setex(city, 300, rendered_page)

                return rendered_page
            else:
                error = "City not found"

    return render_template("index.html", weather=weather, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
