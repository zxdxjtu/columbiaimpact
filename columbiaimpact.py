from flask import Flask
from flask import render_template, redirect

app = Flask(__name__)


@app.route('/')
def hello_world():

    # A flag indicating if user has logged in
    userLoggedIn = False

    context = dict(userLoggedIn = userLoggedIn)

    return render_template("index.html", **context)


if __name__ == '__main__':
    app.run()
