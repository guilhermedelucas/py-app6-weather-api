from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("translator.html")

@app.route("/api/v1/<word>")
def about(word):
    return {
        "word": word,
        "definition": word.upper(),
    }

if __name__ == "__main__":
    app.run(debug=True, port=5002)