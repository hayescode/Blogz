from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://build-a-blog:build-a-blog@localhost:8888/build-a-blog"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

""" class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

tasks = []

@app.route("/", methods=["POST", "GET"])
def index():

    if request.method == "POST":
        task = request.form["task"]
        tasks.append(task)

    return render_template('todos.html', tasks=tasks, title="Get It Done!") """

app.run()