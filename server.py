from flask import Flask, render_template, request, redirect, url_for
import data_manager
import util
from util import question_picker
app = Flask(__name__)


@app.route("/")
@app.route("/list")
def main():
    questions = data_manager.get_saved_data(data_manager.file_path_questions, header=data_manager.questions_header)[1:]
    sorted_questions = data_manager.sort_questions(questions, sort_key="submission_time")
    header = data_manager.get_saved_data(data_manager.file_path_questions, header=data_manager.questions_header)[0]
    return render_template('list.html', questions=sorted_questions, header=header)


@app.route("/question/<question_id>")
def display_a_question(question_id):
    questions = data_manager.get_saved_data(data_manager.file_path_questions, header=data_manager.questions_header)[1:]
    question = util.question_picker(question_id, questions)
    return render_template('display_a_question.html', question=question)


@app.route("/add-questions", methods=['GET', 'POST'])
def add_question():
    questions = data_manager.get_saved_data(data_manager.file_path_questions, header=data_manager.questions_header)
    if request.method == "GET":
        return render_template('add-question.html')
    elif request.method == "POST":
        title = request.form['issue']
        message = request.form['question']
        # util.create_new_question(title, message)
        data_manager.write_to_file(data_manager.file_path_questions, data_manager.questions_header,
                                   util.create_new_question(title, message, questions))

        # valamifunction(request.form)
        # data_manager.write_to_file(file_path_questions, questions_header):
        return redirect("/")



if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,

    )
