from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
import json
from datetime import timedelta

app = Flask(__name__)  # ✅ Fixed the typo here
app.secret_key = "super_secret_key"
app.permanent_session_lifetime = timedelta(minutes=30)

# Load users from JSON
with open("data/users.json") as f:
    USERS = json.load(f)

@app.route("/")
def login_page():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    for user in USERS:
        if user["username"] == username and user["password"] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
    
    # 🟡 Show error on the same login page
    return render_template("index.html", error="Invalid credentials. Please try again.")


@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login_page'))

    username = session.get('user', 'Guest')

    response = make_response(render_template('dashboard.html', username=username))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/logout")
def logout():
    session.clear()
    session.modified = True
    resp = redirect(url_for('login_page'))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7257, debug=True)
