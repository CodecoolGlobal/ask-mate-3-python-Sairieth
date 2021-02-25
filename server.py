from flask import Flask, render_template, request, redirect, url_for
from data_manager import *
from util import *

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
@app.route("/list", methods=['GET', 'POST'])
def main():
    if request.method == "GET":
        questions = get_saved_data(file_path_questions, header=questions_header)[1:]
        # sorted_questions = sort(questions, sort_key="submission_time", direction="ascending")
        header = get_saved_data(file_path_questions, header=questions_header)[0]
        return render_template('list.html', questions=questions, header=header)
    elif request.method == "POST":
        questions = get_saved_data(file_path_questions, header=questions_header)[1:]
        sort_key = request.form['option']
        direction = request.form['order']
        questions = sort(questions, sort_key=sort_key, direction=direction)
        header = get_saved_data(file_path_questions, header=questions_header)[0]
        return render_template('list.html', questions=questions, header=header)


@app.route("/question/<question_id>")
def display_a_question(question_id):
    questions = get_saved_data(file_path_questions, header=questions_header)[1:]
    question = question_picker(question_id, questions)
    answer_data = get_saved_data(file_path_answers, header=answer_header)[1:]
    answers = get_answers(question_id, answer_data)
    return render_template('display_a_question.html', question=question, question_id=question_id, answers=answers)


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


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == "GET":
        questions = get_saved_data(file_path_questions, header=questions_header)[1:]
        question = question_picker(question_id, questions)
        return render_template("edit_question.html", question=question, question_id=question_id)
    if request.method == "POST":
        questions = get_saved_data(file_path_questions, header=questions_header)[1:]
        for question in questions:
            if question["id"] == question_id:
                question["title"] = request.form["title"]
                question["message"] = request.form["message"]
        update_file(file_path_questions, questions_header, questions)
        return redirect(url_for('display_a_question', question_id=question_id))


@app.route("/question/<int:question_id>/new-answer", methods=["GET", "POST"])
def route_add_answer(question_id):
    if request.method == "GET":
        return render_template("new_answer.html", question_id=question_id)
    elif request.method == "POST":
        answers = get_saved_data(file_path_answers, header=answer_header)
        new_answer = {"id": generate_id(answers),
                      "submission_time": get_time(),
                      "vote_number": 0,
                      "question_id": question_id,
                      "message": request.form.get("message")}
        write_to_file(file_path_answers, answer_header, new_answer)
        return redirect(url_for('display_a_question', question_id=question_id))


@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def delete_question(question_id):
    if request.method == 'GET':
        return render_template("delete_question.html", question_id=question_id)
    if request.method == 'POST':
        delete_question_from_file(question_id)
        delete_answer_from_file(question_id)
        return redirect('/')


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer_by_id(answer_id):
    if request.method == 'GET':
        answer_id = request.form.get("answer_id")
        answers = get_saved_data(file_path_answers, header=answer_header)[1:]
        for answer in answers:
            if answer['id'] == answer_id:
                index = answers.index(answer)
                del answers[index]
            update_file(file_path_answers, answer_header, answers)
        return redirect('/question/<question_id>')


@app.route("/question/<question_id>/vote_up")
def question_vote_up(question_id):
    questions = get_saved_data(file_path_questions, header=questions_header)[1:]
    for question in questions:
        if question["id"] == question_id:
            temp_number = int(question['vote_number']) + 1
            question['vote_number'] = str(temp_number)
    update_file(file_path_questions, questions_header, questions)
    return redirect(url_for("main"))


@app.route("/question/<question_id>/vote_down")
def question_vote_down(question_id):
    questions = get_saved_data(file_path_questions, header=questions_header)[1:]
    for question in questions:
        if question["id"] == question_id:
            temp_number = int(question['vote_number']) - 1
            question['vote_number'] = str(temp_number)
    update_file(file_path_questions, questions_header, questions)
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,

    )
