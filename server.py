from flask import Flask, render_template, request
from main import serp

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result")
def results():
    query = request.args.get('q')
    summary = serp(query)
    return render_template("results.html", summary=summary)
