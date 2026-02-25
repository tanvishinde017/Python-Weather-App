from flask import Flask, render_template, request
import requests
import os
import redis
import logging
from dotenv import load_dotenv
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

load_dotenv()

app = Flask(__name__)

# ----------------------------
# Logging
# ----------------------------
logging.basicConfig(level=logging.INFO)

# ----------------------------
# Environment Variables
# ----------------------------
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ----------------------------
# Redis Connection
# ----------------------------
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True
)

# ----------------------------
# Prometheus Metrics
# ----------------------------
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of requests to the weather app"
)

# ----------------------------
# Health Endpoint
# ----------------------------
@app.route("/health")
def health():
    return {"status": "healthy"}, 200

# ----------------------------
# Metrics Endpoint
# ----------------------------
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

# ----------------------------
# Main Route
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    REQUEST_COUNT.inc()  # 🔥 Increment metric counter

    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        if not city:
            error = "Please enter a city name"
        else:
            city = city.strip().lower()
            cache_key = f"weather:{city}"

            logging.info(f"Fetching weather for {city}")

            # Check cache
            cached_weather = redis_client.get(cache_key)
            if cached_weather:
                logging.info("Returning cached result")
                return cached_weather

            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "units": "metric",
                "appid": API_KEY
            }

            try:
                response = requests.get(url, params=params, timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    weather = {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"].title(),
                        "icon": data["weather"][0]["icon"]
                    }

                    rendered_page = render_template("index.html", weather=weather)

                    # Cache for 5 minutes
                    redis_client.setex(cache_key, 300, rendered_page)

                    return rendered_page
                else:
                    error = "City not found"

            except requests.exceptions.RequestException as e:
                logging.error(f"API request failed: {e}")
                error = "Weather service unavailable"

    return render_template("index.html", weather=weather, error=error)

# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)