import os
import openai
from openai.error import RateLimitError
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid
from functools import wraps
from helper import password_check

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
db_engine = create_engine("sqlite:///users.db")
DBSession = sessionmaker(bind=db_engine)
db_session = DBSession()

Base = declarative_base()

# Define User class for ORM
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    hash = Column(String, nullable=False)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_api_key():
    with open('static/key.txt', 'r') as file:
        return file.read().strip()


@app.route("/")
@login_required
def main():
    user_id = session["user_id"]
    return render_template("index.html")


@app.route("/ml", methods=["GET", "POST"])
@login_required
def ml():
    if request.method == "POST":
        email = request.form.get("email")
        # Check if email is in field
        if not email:
            return render_template("ml.html", missing=True, alreadyindb=False, success=False)

        # Check if Email is already in DB
        existing_email = db.execute("SELECT id FROM ml_notify WHERE email = ?", email)
        if existing_email:
            return render_template("ml.html", missing=False, alreadyindb=True, success=False)
        else:
            db.execute("INSERT INTO ml_notify (email) VALUES (?)", email)
            return render_template("ml.html", missing=False, alreadyindb=False, success=True)
    else:
        return render_template("ml.html", missing=False, alreadyindb=False, success=False)



@app.route('/chat', methods=["GET", 'POST'])
@login_required
def bot_response():
    api_key = get_api_key()
    if request.method == "POST":
        if request.headers.get('API-Key') == api_key:
            data = request.get_json()
            user_message = data['message']

            # Use OpenAI GPT-3.5-turbo to generate the bot's response based on the user_message
            openai.api_key = get_api_key()  # Replace with your actual OpenAI API key
            prompt = "User: " + user_message + "\nBot:"

            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",  # Use "text-davinci-003" for GPT-3.5-turbo
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=150,
                    n=1,
                    stop=["\n"]
                )
                bot_response = response.choices[0].text.strip()
            except Exception as e:
                print("Error while calling OpenAI API:", e)
                bot_response = "Sorry, I'm having trouble generating a response right now. Please try again later."

            return jsonify({'response': bot_response})
        else:
            return jsonify({'error': 'Unauthorized'}), 401
    else:
        return render_template("ai.html")

@app.route("/forgot-password", methods=["GET", "POST"])
def resetpw():
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            return render_template("forgot-password.html", cred=True, existing=False)

        existing_user = db.execute("SELECT id FROM user_details WHERE email = ?", email)
        if not existing_user:
            return render_template("forgot-password.html", existing=True, cred=False)
    else:
        return render_template("forgot-password.html", existing=False, cred=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        # check usernme
        if not request.form.get("username"):
            return render_template("login.html", cred=True)
        # check psw
        if not request.form.get("password"):
            return render_template("login.html", cred=True)

        if request.form.get("stay_logged_in"):
            app.config["SESSION_PERMANENT"] = True


        # Check database
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("login.html", cred=False)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return render_template("register.html", cred=True, safe={'password_ok': True}, notsame=False)

        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html", notsame=True, safe={'password_ok': True}, cred=True)

        safe = password_check(request.form.get("password"))

        # Check for password errors and render the appropriate template
        if not safe['password_ok']:
            if safe['length_error']:
                return render_template("register.html", safe=safe, length_error=True)
            elif safe['digit_error']:
                return render_template("register.html", safe=safe, digit_error=True)
            elif safe['uppercase_error']:
                return render_template("register.html", safe=safe, uppercase_error=True)
            elif safe['lowercase_error']:
                return render_template("register.html", safe=safe, lowercase_error=True)
            elif safe['symbol_error']:
                return render_template("register.html", safe=safe, symbol_error=True)

        # Check if the username already exists in the database
        existing_user = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        if existing_user:
            return render_template("register.html", existing=True, safe={'password_ok': True}, notsame=False)

        # Check mail
        existing_user_email = db.execute("SELECT id FROM user_details WHERE email = ?", request.form.get("email"))
        if existing_user_email:
            return render_template("register.html", mailexisting=True, existing=False, safe={'password_ok': True}, notsame=False)

        # Hash the password and insert the new user into the database
        hashp = generate_password_hash(request.form.get("password"), method="pbkdf2", salt_length=16)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hashp)

        # Insert details into second table
        user_row = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        users_id = user_row[0]["id"]

        db.execute("INSERT INTO user_details (id, first_name, last_name, email) VALUES (?, ?, ?, ?)",
                users_id, request.form.get("firstname"), request.form.get("surname"), request.form.get("email"))

        return redirect("/")

    else:
        return render_template("register.html", safe={'password_ok': True}, notsame=False)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("80"), debug=True)
