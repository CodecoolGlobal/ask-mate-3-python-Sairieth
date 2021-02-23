from flask import Flask, render_template, request, redirect, url_for
import data_manager
app = Flask(__name__)


@app.route("/")
@app.route("/list")
def main():
    questions = data_manager.get_saved_data(data_manager.file_path_questions, header=data_manager.questions_header)[1:]
    sorted_questions = data_manager.sort_questions(questions, sort_key="submission_time")
    header = data_manager.get_saved_data(data_manager.file_path_questions, header=data_manager.questions_header)[0]
    return render_template('list.html', questions=sorted_questions, header=header)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,

    )
