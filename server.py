from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from util import *
from data_manager import *
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def list_question():
    return render_template("list.html")


@app.route('/add-questions', methods=["GET"])
def route_question():
    return render_template("add-question.html",
                           title="Add question")


@app.route('/add_questions', methods=["POST"])
def add_question():
    new_question = {"view_number": 0,
                    "vote_number": 0,
                    "title": request.form.get("title"),
                    "message": request.form.get("message"),
                    "image": None}
    add_a_question(new_question)
    return redirect("/")


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
