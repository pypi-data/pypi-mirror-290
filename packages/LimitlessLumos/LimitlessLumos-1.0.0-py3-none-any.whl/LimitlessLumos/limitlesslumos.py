from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)


@app.route('/')
def root():
    return render_template("server.html")


def run():
    app.run(host='0.0.0.0')


def lumosServer():
    t = Thread(target=run)
    t.start()


if __name__ == '__main__':
    lumosServer()
