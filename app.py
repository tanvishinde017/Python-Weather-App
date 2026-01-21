from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "c1e17822e800e0bf45c4560fc10fb2b2"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    temp_c = None
    city = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name"
        else:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={API_KEY}"
            response = requests.get(url).json()

            if response.get("cod") == "404":
                error = "City not found"
            else:
                weather = response["weather"][0]["main"]
                temp_f = response["main"]["temp"]
                temp_c = round((temp_f - 32) * 5 / 9, 2)

    return render_template(
        "index.html",
        weather=weather,
        temp_c=temp_c,
        city=city,
        error=error
    )

if __name__ == "__main__":
    app.run()
