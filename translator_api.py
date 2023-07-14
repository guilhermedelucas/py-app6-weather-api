from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("translator.html")


@app.route("/api/v1/<word>")
def about(word):
    dictionary = pd.read_csv('dictionary.csv', sep=',')
    definition = dictionary.loc[dictionary['word'] == word]['definition'].squeeze()
    return {
        "word": word,
        "definition": definition,
    }

if __name__ == "__main__":
    app.run(debug=True, port=5002)