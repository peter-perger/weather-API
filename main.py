from flask import Flask, render_template
import pandas as pd


app = Flask("website")
app.json.sort_keys = False


# df = pd.read_csv("")


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    station_string = str(station).zfill(6)
    path = f"data_small\TG_STAID{station_string}.txt"

    df = pd.read_csv(path, skiprows=20, parse_dates=["    DATE"])

    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    print(temperature)

    result_dict = {
        "station": station,
        "date": date,
        "temperature": temperature
    }

    return result_dict


if __name__ == "__main__":
    app.run(debug=True)
