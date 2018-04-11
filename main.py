from flask import Flask, request, redirect, render_template, flash
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

@app.route("/blog", methods=["POST", "GET"])
def index():
    blog_id = request.args.get("id")
    if blog_id:
        blog = Blog.query.filter_by(id=blog_id).all()
        return render_template("blog.html",blogs=blog)

    else:
        blogs = Blog.query.filter_by().all()    #gets all blogs
        title = "Build A Blog"
        return render_template('blog.html',blogs=blogs, title=title)    #removing title will break if/else in blog.html

@app.route("/newpost", methods=["POST","GET"])
def newpost():
    if request.method == "POST":    #if submitting a new blog, validate.
        title = request.form["title"]
        content = request.form['content']
        if title == "" or content == "":
            flash("You must fill in a title and some content","error")
            return render_template('newpost.html',title=title,content=content)
        else:
            new_blog = Blog(title,content)  #<---add author to this
            db.session.add(new_blog)
            db.session.commit()     #add to db
            this_blog = Blog.query.filter_by(title=title).all() #select blog we just added
            blog_id = this_blog[0].id   #get the id of the blog we just added
            blog_url = "blog?id=" + str(blog_id)    #concat into GET url
            return redirect(blog_url)
    else:   #if just trying to type a new blog, skip validation
        return render_template('newpost.html')

@app.route("/login", methods=["POST","GET"])
def login():
    #something
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash("logged in")
            return redirect("/")
        else:
            flash("user password incorrect, or user does not exist", "error")
            
    return render_template("login.html")

@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]

        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect("/")
        else:
            #tell user they're already registered
            return "<h1>Error! Already Registered!</h1>"
            
    return render_template("signup.html")

if __name__ == "__main__":
    app.run()