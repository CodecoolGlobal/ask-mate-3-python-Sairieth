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
        questions = get_all_questions_by_order(attribute, order)
        return render_template('list.html', questions=questions)
    else:
        questions = get_all_questions()
        return render_template('list.html', questions=questions)


@app.route("/question/<question_id>")
def display_a_question(question_id):
    question = get_question(question_id)
    answers = get_answer(question_id)
    comments = get_all_comments(question_id)
    #temp_view_number = int(question['view_number']) + 1
    #question['view_number'] = temp_view_number
    #update_file(file_path_questions, questions_header, questions)
    return render_template('display_a_question.html', question=question, question_id=question_id, answers=answers, comments=comments)


@app.route('/question/<question_id>/vote_up')
def vote_up_question(question_id):
    question_vote_up(question_id)
    return redirect(url_for("main"))


@app.route('/question/<question_id>/vote_down')
def vote_down_question(question_id):
    question_vote_down(question_id)
    return redirect(url_for("main"))



@app.route('/answer/<answer_id>/vote_up')
def vote_up_answer(answer_id):
    answer_vote_up(answer_id)
    question_id = get_question_id(answer_id)['question_id']
    return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/answer/<answer_id>/vote_down')
def vote_down_answer(answer_id):
    answer_vote_down(answer_id)
    question_id = get_question_id(answer_id)['question_id']
    return redirect(url_for("display_a_question", question_id=question_id))


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


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def new_question_comment(question_id):
    pass


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
