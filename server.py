from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import time
import re
import md5

app = Flask(__name__)
app.secret_key = "waow"
mysql = MySQLConnector(app,'reddit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.route('/')
def index():
    if not "loggedOn" in session:
        session["loggedOn"] = False
    if not "username" in session:
        session["username"] = " "
    print session['username']
    print session['loggedOn']
    
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

@app.route('/<sub>')
def subs(sub):
    check = "SELECT * FROM subreddits"
    for i in (mysql.query_db(check)):
        if i['url'] == sub:
            print "turd"
            current_id = i['id']
            query = "SELECT text, title FROM posts WHERE subreddit_id = {}".format(current_id)
            posts = mysql.query_db(query)
            return render_template('subs.html', posts = posts)
    '''
    make a query to retrieve top posts from particular sub

    if logged in, give the user an option to follow that subreddit. Also maybe
    add functionality to unsubscribe
        -this will require a seperate post route
    '''
    #if we do not find the specified page, we render the 404 page
    return render_template('404.html')



@app.route('/register')
def register():
    '''
    pretty much just render the registration page but make it look pretty. When
    registration is complete, render the user page
    '''
    return render_template('register.html')

@app.route('/byeFelicia', methods = ['POST'])
def logoff():
    session['loggedOn'] = False
    session['username'] = ""
    return redirect('/')

@app.route('/logAndReg', methods=['POST'])
def logAndReg():
    if request.form['action'] == 'signIn':
        username = request.form['username']
        password = request.form['password']
        hashed_password = md5.new(password).hexdigest()
        check = "SELECT * FROM users"
        
        for i in (mysql.query_db(check)):
            #change password to hashed_password below
            if i['username'] == username and i['password'] == hashed_password:
                session['loggedOn'] = True
                session['username'] = username
                flash("Welcome {}!".format(i['username']))
                return redirect('/')
        flash('incorrect username/password combo')
        return redirect('/')

        '''
        1) make a query call to see if both the username are in the db and that they
        belong to the same user
        2) if not, redirect to index and set a flash message for incorrect login
        '''

    else:
        #get data from forms
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = md5.new(password).hexdigest()
        confirm = request.form['confirm']
        

        data = { #change password to hashed_password below
                'username': username,
                'email': email,
                'password': hashed_password
                }
        #set all data in a dictionary
        
        query = "INSERT INTO users (username, email, password) VALUES (:username, :email, :password)"
        
        properLogin = True

        check = "SELECT * FROM users"
        if len(username) < 1:
            flash("Please enter a username")
            properLogin = False
        for i in (mysql.query_db(check)):
            if i['username'] == username:
                flash("Username already in database")
                properLogin = False

        my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        check = "SELECT * FROM users"
        for i in (mysql.query_db(check)):
            if i['email'] == email:
                flash("email already in database")
                properLogin = False
        if not my_re.match(email):
            flash("please use a proper email")
            properLogin = False
        
        if len(password) < 8:
            flash("password must be at least 8 characters long")
            properLogin = False
        if password != confirm:
            flash("passwords must match")
            properLogin = False
        
        if properLogin:
            mysql.query_db(query, data)
            flash("Welcome to this pointless website {}!".format(username))
            session['loggedOn'] = True
            session['username'] = username
            return redirect('/')
        else:
            return redirect('/register')

@app.route('/users')
def users():
    '''
    display all of the users information. IE the users posts and comments and
    messages from other users.
    '''
    return render_template('users.html')

@app.route('/posts/<sub>/<post>')
def posts(sub, post):
   
        
    '''
    render any aplicable photo or video

    render comments
    '''
    return render_template('posts.html')

@app.route('/newSub')
def newSub():
    '''
    make a query to retrieve top posts from particular sub

    if logged in, give the user an option to follow that subreddit. Also maybe
    add functionality to unsubscribe
    '''
    return redirect('/')

@app.route('/submit')
def submit():
    return render_template('submit.html')

@app.route('/newPost', methods=['POST'])
def newPost():
    if request.form['title']:
        title = request.form['title']
    else:
        flash("fields may not be blank")
        return redirect('/submit')
    if request.form['text']:
        text = request.form['text']
    else:
        flash("fields may not be blank")
        return redirect('/submit')
    if request.form['sub']:
        sub = request.form['sub']
    else:
        flash("fields may not be blank")
        return redirect('/submit')

    #fetches current user ID
    q1 = "SELECT id FROM users where username = '{}'".format(session['username'])
    d1 = mysql.query_db(q1)
    current_id = d1[0]['id']
    print current_id

    #fetches current sub ID
    q2 = "SELECT id FROM subreddits where url = '{}'".format(sub)
    d2 = mysql.query_db(q2)
    if d2:
        current_sub = d2[0]['id']
    

    data = {'title': title,
            'text': text,
            'url': sub,
            'id': current_id,
            }

    check = "SELECT * FROM subreddits"
    for i in (mysql.query_db(check)):
        if i['url'] == sub:
            print "we here"
            data['subID'] = current_sub
            print data['subID']
            query2 = "INSERT INTO posts (text, user_id, subreddit_id, created_at, title) VALUES (:text, :id, :subID, NOW(), :title)"
            mysql.query_db(query2, data)
            return redirect('/')

    #insert into database if new subreddit
    #adds subreddit
    query1 = "INSERT INTO subreddits (url, created_at) VALUES (:url, NOW())"
    mysql.query_db(query1, data)
    #retrieves subreddit id
    q3 = "SELECT id FROM subreddits where url = '{}'".format(sub)
    d3 = mysql.query_db(q3)
    print d3
    if d3:
        current_sub = d3[0]['id']
    data['subID'] = current_sub
    query2 = "INSERT INTO posts (text, user_id, subreddit_id, created_at) VALUES (:text, :id, :subID, NOW())"
    mysql.query_db(query2, data)
    return redirect('/')


app.run(debug=True)
