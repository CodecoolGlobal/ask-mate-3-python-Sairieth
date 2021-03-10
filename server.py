from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from util import *
from data_manager import *
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def list_question():
    return render_template("list.html")


@app.route('/add_questions', methods=['GET', "POST"])
def add_question():
    if request.method == 'GET':
        return render_template("add-question.html")
    if request.method == 'POST':
        new_question = {"view_number": 0,
                        "vote_number": 0,
                        "title": request.form.get("title"),
                        "message": request.form.get("message"),
                        "image": None}
        add_a_question(new_question)
        return redirect("/")


@app.route('/question/<question_id>/delete', methods=['GET', "POST"])
def delete_question(question_id):
    if request.method == 'GET':
        return render_template("delete_question.html", question_id=question_id)
    if request.method == 'POST':
        delete_a_question(question_id)
        return redirect('/')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
