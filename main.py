from flask import Flask, render_template
import pandas

app = Flask(__name__)

stations = pandas.read_csv(f"data_small/stations.txt", skiprows=16)
stations.rename(columns={'STANAME                                 ': 'STANAME' }, inplace=True)
stations = stations[['STAID', 'STANAME']]

@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    df = pandas.read_csv(f"data_small/TG_STAID{str(station).zfill(6)}.txt", skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }


if __name__ == "__main__":
    app.run(debug=True, port=5001)