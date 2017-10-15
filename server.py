from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import time
import re

app = Flask(__name__)
app.secret_key = "waow"
#mysql = MySQLConnector(app,'redditdb')

@app.route('/')
def index():
    '''
    make a query to fetch the top rated posts from the database and pass
    them into the html page.

    check to see if someone is logged in. If so, have a link that takes them
    to their user page

    if not logged in give display a login form and a option to register

    make query to fetch top subreddits. display the most popular subs at the
    top of the page

    if time, add a search bar to look for subreddits
    '''
    return render_template('index.html')

@app.route('/subs')
def subs():
    '''
    make a query to retrieve top posts from particular sub

    if logged in, give the user an option to follow that subreddit. Also maybe
    add functionality to unsubscribe
    '''
    return render_template('subs.html')

@app.route('/register')
def register():
    '''
    pretty much just render the registration page but make it look pretty. When
    registration is complete, render the user page
    '''
    return render_template('register.html')

@app.route('/users')
def users():
    '''
    display all of the users information. IE the users posts and comments and
    messages from other users.
    '''
    return render_template('users.html')

@app.route('/posts')
def posts():
    '''
    render any aplicable photo or video

    render comments
    '''
    return render_template('posts.html')

@app.route('/submit')
def submit():
    '''
    Probably take code from registration form and format to better fit the fields 
    for submission
    '''
    return render_template('submit.html')

# @app.route('/process', methods=['POST']) 
# def create():
#     email = request.form['email']
#     data ={'email': email}
#     query = "INSERT INTO emails (email, created_at) VALUES (:email, NOW())"
#     check = "SELECT * FROM emails"
#     print mysql.query_db(check)

#     my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#     for i in (mysql.query_db(check)):
#         if i['email'] == email:
#             flash("email already in database")
#             return redirect('/')
#     if not my_re.match(email):
#         flash("bad email")
#     else:
#         print "good email"
#         mysql.query_db(query, data)
#         return redirect('/success')
#     return redirect('/')

# @app.route('/success')
# def success():
#     query = "SELECT email, created_at FROM emails"
#     emails = mysql.query_db(query)

#     return render_template("success.html", emails = emails)





# @app.route('/friends/<friend_id>')
# def show(friend_id):
#     query = "SELECT * FROM friends WHERE id = :specific_id"
#     data = {'specific_id': friend_id}
#     friends = mysql.query_db(query, data)
#     return render_template('index.html', one_friend=friends[0])

    

app.run(debug=True)
