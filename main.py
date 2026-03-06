from flask import Flask, render_template
import pandas as pd


app = Flask("website")
app.json.sort_keys = False


stations = pd.read_csv("data_small\stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


@app.route('/')
def home():
    return render_template("home.html", data=stations.to_html(),)


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    station_string = str(station).zfill(6)
    path = f"data_small\TG_STAID{station_string}.txt"

    df = pd.read_csv(path, skiprows=20, parse_dates=["    DATE"])

    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10

    result_dict = {
        "station": station,
        "date": date,
        "temperature": temperature
    }

    return result_dict


@app.route("/api/v1/<station>")
def all_data(station):
    station_string = str(station).zfill(6)
    path = f"data_small\TG_STAID{station_string}.txt"

    df = pd.read_csv(path, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")

    return result


@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    station_string = str(station).zfill(6)
    path = f"data_small\TG_STAID{station_string}.txt"

    df = pd.read_csv(path, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))]

    print(result)

    return result.to_dict(orient="records")


if __name__ == "__main__":
    app.run(debug=True)
