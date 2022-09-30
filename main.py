# micro web framework to develop websites with python
# on cmd "pip install flask"
# import request
# import session
# import flash
# import sqlalchemy instal sqlalchemy

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # creates web application instance
app.secret_key = "Orange" # decrypt and encrypt the data
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3" #reference the users table
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #not track all modifications to database and no warnings
app.permanent_session_lifetime = timedelta(minutes = 2) # stores permanent session data for a time period given

db = SQLAlchemy(app) # database object which is equal to a sql database
# with sqlalchemy write all queries in python code rather than SQL

class users(db.Model): # inherit from here
    _id = db.Column("id", db.Integer, primary_key=True) #every object in database needs a unique identification
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/") # defines how to access the page e.g. yahya.com/
def home(): # new page needs a function
    return render_template("index.html")

# @app.route("/view")
# def view():
#     return render_template

@app.route("/login", methods=["POST", "GET"]) # GET - receiving/sending information to a client/website, POST - secure method of GET where info not stored on webserver
def login():
    if request.method == "POST": # when information inputted (POST) by user into the site redirects to the url
        session.permanent = True # adds permanent stay time for session
        user = request.form["nm"] # user is the input by the user on the site
        session["user"] = user # session stores the user input data, closing the browser will delete session data

        found_user = users.query.filter_by(name=user).first() # find the users in the table that have a name from the first entry
        if found_user:
            session["email"] = found_user.email # grab user email and store in the session
        else:
            usr = users(user, None)
            db.session.add(usr) # add user model to the database
            db.session.commit() # everytime change to database commit the changes

        flash(f"You have been logged in!", "info") # shows message once
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash(f"Already logged in!", "info")
            return redirect(url_for("user")) # if logged in redirect to user page not go to login page
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"]) # receive info on user page
def user():
    email = None
    if "user" in session: # user is in session
        user = session["user"]

        if request.method == "POST": # if POST request is made the email is grabbed from the field
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email # change the users email
            db.session.commit()
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email = email) # direct to user page
    else:
        flash(f"You are not logged in.", "info")
        return redirect(url_for("login")) # redirects to  login page if user not in session

@app.route("/logout")
def logout():
    flash(f"You have been logged out!", "info")
    session.pop("user", None) # remove user data from session
    session.pop("email", None) # remove email once user logs out
    return redirect(url_for("login"))

if __name__ == "__main__": # will run the app
    db.create_all()
    app.run(debug=True) # no need to rerun server if there are changes as it will automatically detect the changes

#https://rapidapi.com/blog/best-recipe-sites/
#https://rapidapi.com/blog/build-food-website/