from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)
app.secret_key = 'oaieitoqhwgasd'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    content = db.Column(db.String(10000))

    def __init__(self, title, content):
        self.title = title
        self.content = content

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
            new_blog = Blog(title,content)  #if title/content is there, create blog
            db.session.add(new_blog)
            db.session.commit()     #add to db
            this_blog = Blog.query.filter_by(title=title).all() #select blog we just added
            blog_id = this_blog[0].id   #get the id of the blog we just added
            blog_url = "blog?id=" + str(blog_id)    #concat into GET url
            return redirect(blog_url)
    else:   #if just trying to type a new blog, skip validation
        return render_template('newpost.html')

if __name__ == "__main__":
    app.run()