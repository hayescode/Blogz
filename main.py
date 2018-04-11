from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://Blogz:Blogz@localhost:8889/blogz"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)
app.secret_key = 'oaieitoqhwgasd'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    content = db.Column(db.String(10000))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref="author")

    def __init__(self, username, password):
        self.username = username
        self.password = password

def logged_in_user():   #checks if a user is logged in. If so, it returns the username.
    try:
        logged_in_user = session["username"]
        return logged_in_user
    except KeyError:
        return None

@app.route("/blog", methods=["POST", "GET"])
def index(): 
    blog_id = request.args.get("id")
    if blog_id:
        blog = Blog.query.filter_by(id=blog_id).all()
        return render_template("blog.html",blogs=blog, logged_in_user=logged_in_user())
    else:
        title = "Blogz"
        blogs = Blog.query.filter_by().all()
        return render_template("blog.html",blogs=blogs,title=title, logged_in_user=logged_in_user())

@app.route("/newpost", methods=["POST","GET"])
def newpost():
    if request.method == "POST":    #if submitting a new blog, validate.
        title = request.form["title"]
        content = request.form['content']
        author = User.query.filter_by(username=logged_in_user()).first()
        if title == "" or content == "":
            flash("You must fill in a title and some content","error")
            return render_template('newpost.html',title=title,content=content, logged_in_user=logged_in_user())
        else:
            new_blog = Blog(title,content,author)  #<---add author to this
            db.session.add(new_blog)
            db.session.commit()     #add to db
            this_blog = Blog.query.filter_by(title=title).all() #select blog we just added
            blog_id = this_blog[0].id   #get the id of the blog we just added
            blog_url = "blog?id=" + str(blog_id)    #concat into GET url
            return redirect(blog_url)
    else:   #if just trying to type a new blog, skip validation
        return render_template('newpost.html', logged_in_user=logged_in_user())

@app.route("/login", methods=["POST","GET"])
def login():    #login functionality
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        username_error = ""
        bad_password_error = ""

        user = User.query.filter_by(username=username).first()

        if not user:
            username_error = "This username has not been registered!"
            return render_template("login.html", username_error=username_error, logged_in_user=logged_in_user()) 

        if user.password != password:   #password is incorrect
            bad_password_error = "You entered the wrong password!"
            return render_template("login.html", username=username, bad_password_error=bad_password_error, logged_in_user=logged_in_user()) 

        if user and user.password == password:  #success! continue on to /newpost logged into session
            session['username'] = username
            flash("logged in")
            return redirect("/newpost")
        

        else:
            flash("user password incorrect, or user does not exist", "error")
            
    return render_template("login.html", logged_in_user=logged_in_user())

@app.route("/signup", methods=["POST","GET"])
def signup():   #registration functionality
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]

        blanks_error = ""
        username_exists_error = ""
        password_match_error = ""
        length_error = ""

        existing_user = User.query.filter_by(username=username).first()

        if username == "" or password == "" or verify =="":
            blanks_error = "You must fill in all fields!"
            return render_template("signup.html", blanks_error=blanks_error, logged_in_user=logged_in_user())

        if len(username) < 3 or len(password) < 3:
            length_error = "Username and password must be at least 3 characters"
            return render_template("signup.html", length_error=length_error, logged_in_user=logged_in_user())

        if password != verify:
            password_match_error = "Your passwords do not match!"
            return render_template("signup.html", password_match_error=password_match_error, logged_in_user=logged_in_user())

        if existing_user.username == username:
            username_exists_error = "This username already exists!"
            return render_template("signup.html", username_exists_error=username_exists_error, logged_in_user=logged_in_user())

        if not existing_user:
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect("/newpost")

    else: #returns template if GET request (trying to sign up first time)
        return render_template("signup.html", logged_in_user=logged_in_user())

@app.route("/logout", methods=["POST","GET"])
def logout():
    del session["username"]
    blogs = Blog.query.filter_by().all()    #gets all blogs
    title = "Blogz"
    return render_template('blog.html',blogs=blogs, title=title, logged_in_user=logged_in_user()) #removing title breaks if/else in blog.html

if __name__ == "__main__":
    app.run()