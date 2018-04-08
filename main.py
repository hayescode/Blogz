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

    blogs = Blog.query.filter_by().all()

    return render_template('blog.html',blogs=blogs)

@app.route("/newpost", methods=["POST","GET"])
def newpost():

    if request.method == "POST":
        title = request.form["title"]
        content = request.form['content']
        if title == "" or content == "":
            flash("You must fill in a title and some content","error")
            return render_template('newpost.html')
        else:
            new_blog = Blog(title,content)
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog")

    else:
        return render_template('newpost.html')

if __name__ == "__main__":
    app.run()