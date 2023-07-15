from flask import Flask, render_template
import pandas

app = Flask(__name__)

stations = pandas.read_csv(f"data_small/stations.txt", skiprows=16)
stations.rename(columns={'STANAME                                 ': 'STANAME' }, inplace=True)
stations = stations[['STAID', 'STANAME']]

@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


def get_station_data(station, skiprows=20, parse_dates=True):
    if parse_dates:
        df = pandas.read_csv(f"data_small/TG_STAID{str(station).zfill(6)}.txt", skiprows=skiprows, parse_dates=['    DATE'])
    else:
        df = pandas.read_csv(f"data_small/TG_STAID{str(station).zfill(6)}.txt", skiprows=skiprows)
    df.rename(columns={
        '    DATE': 'DATE',
        '   TG': 'TG',
        ' Q_TG': 'Q_TG',
        ' SOUID': 'SOUID',
    }, inplace=True)
    return df

@app.route("/api/v1/<station>")
def data(station):
    df = get_station_data(station, skiprows=20)
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    df = get_station_data(station, skiprows=20)
    temperature = df.loc[df['DATE'] == date]['TG'].squeeze() / 10
    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }


@app.route("/api/v1/year/<station>/<year>")
def yearly(station, year):
    df = get_station_data(station, skiprows=20, parse_dates=False)
    print(df)
    df['DATE'] = df['DATE'].astype(str)
    result = df[df['DATE'].str.startswith(str(year))].to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True, port=5001)