from flask import Flask
from flask import render_template, redirect
from flask import request


app = Flask(__name__)


@app.route('/')
def hello_world():

    context = dict()

    return render_template("index.html", **context)


@app.route('/addBathroom', methods=['GET', 'POST'])
def add_bathroom():

    context = dict()

    return render_template("addBathroom.html", **context)


if __name__ == '__main__':
    app.run()
