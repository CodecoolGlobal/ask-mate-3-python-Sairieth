from flask import Flask, render_template, request, redirect, url_for
import data_manager
app = Flask(__name__)


@app.route("/")
@app.route("/list")
def main():
    questions =
    return render_template('list' )



if __name__ == "__main__":
    app.run()
