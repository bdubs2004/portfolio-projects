from flask import Flask, render_template, request, redirect, url_for
from google.cloud import datastore
import re

app = Flask(__name__)
datastore_client = datastore.Client()

def add_entry(name, weight, wins, losses, pins):
    key = datastore_client.key("WeightEntry")
    entry = datastore.Entity(key)
    entry.update({
        "name": name,
        "weight": float(weight),
        "wins": int(wins),
        "losses": int(losses),
        "pins": int(pins)
    })
    datastore_client.put(entry)

def get_entries(filters=None):
    query = datastore_client.query(kind="WeightEntry")
    if filters:
        for key, value in filters.items():
            query.add_filter(key, "=", value)
    return list(query.fetch())

def delete_entry(entry_id):
    key = datastore_client.key("WeightEntry", entry_id)
    datastore_client.delete(key)

def is_valid_name(name):
    return re.match(r"^[A-Za-z ]+$", name)

def is_valid_weight(weight):
    try:
        weight = float(weight)
        return 80.0 <= weight <= 400.0
    except ValueError:
        return False

def is_valid_number(value):
    try:
        return int(value) >= 0
    except ValueError:
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/log_weight", methods=["GET", "POST"])
def log_weight():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        weight = request.form.get("weight", "").strip()
        wins = request.form.get("wins", "0").strip()
        losses = request.form.get("losses", "0").strip()
        pins = request.form.get("pins", "0").strip()

        if not (name and weight and wins and losses and pins):
            return render_template("log_weight.html", error="All fields are required!")

        if not is_valid_name(name):
            return render_template("log_weight.html", error="Name must contain only letters and spaces!")

        if not is_valid_weight(weight):
            return render_template("log_weight.html", error="Weight must be between 80 and 400 lbs!")

        if not (is_valid_number(wins) and is_valid_number(losses) and is_valid_number(pins)):
            return render_template("log_weight.html", error="Wins, losses, and pins must be non-negative numbers!")

        add_entry(name, weight, wins, losses, pins)
        return redirect(url_for("view_entries"))

    return render_template("log_weight.html")

@app.route("/entries", methods=["GET", "POST"])
def view_entries():
    filters = {}
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        weight = request.form.get("weight", "").strip()
        if name:
            filters["name"] = name
        if weight:
            try:
                filters["weight"] = float(weight)
            except ValueError:
                pass

    entries = get_entries(filters)
    return render_template("entries.html", entries=entries)

@app.route("/delete_entry/<int:entry_id>", methods=["POST"])
def delete_entry_route(entry_id):
    delete_entry(entry_id)
    return redirect(url_for("view_entries"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
