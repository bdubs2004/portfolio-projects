from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

registrants = []  # Store registered users

SPORTS = ["Dodgeball", "Flag Football", "Soccer", "Volleyball", "Ultimate Frisbee"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        sport = request.form.get("sport", "")

        # Validate inputs
        if not name:
            return render_template("register.html", sports=SPORTS, error="Name is required.")

        if sport not in SPORTS:
            return render_template("register.html", sports=SPORTS, error="Invalid sport selection.")

        registrants.append({"name": name, "sport": sport})

        return redirect(url_for("view_registrants"))

    return render_template("register.html", sports=SPORTS)

@app.route("/registrants")
def view_registrants():
    return render_template("registrants.html", registrants=registrants)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)  # Debug enabled for development
