from flask import Flask, render_template, request, redirect, url_for
from data_manager import *
from util import *

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def main():
    questions = get_saved_data(file_path_questions, header=questions_header)[1:]
    sorted_questions = sort_questions(questions, sort_key="submission_time")
    header = get_saved_data(file_path_questions, header=questions_header)[0]
    return render_template('list.html', questions=sorted_questions, header=header)


@app.route("/question/<question_id>")
def display_a_question(question_id):
    questions = get_saved_data(file_path_questions, header=questions_header)[1:]
    question = question_picker(question_id, questions)
    return render_template('display_a_question.html', question=question, question_id=question_id)


@app.route("/add-questions", methods=['GET', 'POST'])
def add_question():
    questions = get_saved_data(file_path_questions, header=questions_header)
    if request.method == "GET":
        return render_template('add-question.html')
    elif request.method == "POST":
        title = request.form['issue']
        message = request.form['question']
        # util.create_new_question(title, message)
        write_to_file(file_path_questions, questions_header, create_new_question(title, message, questions))
        return redirect("/")


# nem lehet 1 route alatt behívni a GET és POST methodot mert valamiért ütközik
@app.route("/question/<int:question_id>/new-answer", methods=["GET"])
def route_add_answer(question_id):
    return render_template("new_answer.html", question_id=question_id)


# TODO rendbe tenni a redirectet
@app.route("/question/<question_id>/new-answer", methods=['POST'])
def add_new_answer(question_id):
    questions = get_saved_data(file_path_questions, header=questions_header)
    answers = get_saved_data(file_path_answers, header=answer_header)
    new_answer = {"id": generate_id(answers),
                  "submission_time": get_time(),
                  "vote_number": 0,
                  "question_id": question_id,
                  "message": request.form.get("message")}

    write_to_file(file_path_answers, answer_header, new_answer)
    return redirect('/')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,

    )
