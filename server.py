from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from data_manager import *
from util import *
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super secret key'

@app.route("/")
@app.route("/list")
def main():
    attribute = request.args.get('attribute')
    order = request.args.get('order')

    if attribute and order:
        questions = get_questions_by_order(attribute, order)
        return render_template('list.html', questions=questions)
    else:
        questions = get_questions()
        return render_template('list.html', questions=questions)


@app.route("/question/<question_id>")
def display_a_question(question_id):
    question = get_question(question_id)
    answers = get_answer(question_id)
    #temp_view_number = int(question['view_number']) + 1
    #question['view_number'] = temp_view_number
    #update_file(file_path_questions, questions_header, questions)
    return render_template('display_a_question.html', question=question, question_id=question_id, answers=answers)


@app.route('/question/<question_id>/vote_up')
def vote_up_question(question_id):
    vote_up(question_id)
    return redirect(url_for("list_question"))


@app.route('/question/<question_id>/vote_down')
def vote_down_question(question_id):
    vote_down(question_id)
    return redirect(url_for("list_question"))

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )