from flask import Flask, render_template, request, redirect, url_for, \
    flash, send_from_directory, make_response, session, Markup
from data_manager import *
from werkzeug.utils import secure_filename
import os
import random
import datetime
import bcrypt

import util
import bcrypt

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super secret key'


@app.route('/')
def get_last_5_question_ordered_by_time():
    questions = get_last_5()
    return render_template("list.html", questions=questions)


@app.route("/list")
@app.route("/search")
def main():
    attribute = request.args.get('attribute')
    order = request.args.get('order')
    phrase = request.args.get('phrase')
    if attribute and order:
        questions = get_all_questions_by_order(attribute, order)
        return render_template('list.html', questions=questions)
    elif phrase:
        questions = get_question_by_phrase(phrase)
        answers = get_answers_by_phrase(phrase)
        tag = Markup(f"<mark>{phrase}</mark>")
        return render_template("list.html", questions=questions, answers=answers, phrase=phrase, tag=tag)
    else:
        questions = get_all_questions()
        return render_template('list.html', questions=questions)


@app.route("/users")
def list_users():
    if "username" in session:
        users = get_all_users()
        return render_template('users.html', users=users)
    else:
        return redirect(url_for("main"))


@app.route('/user/<user_id>')
def get_user_page(user_id):
    if "username" in session:
        user_details = get_user_details(user_id)
        user_questions = get_user_questions(user_id)
        user_answers = get_user_answers(user_id)
        user_question_comments = get_comments_for_question(user_id)
        user_answer_comments = get_comment_for_answer(user_id)
        # for answer in user_answers:
        #     answer_comment = get_comment_for_answer(answer_id=answer['answer_id'])
        #     answer["comment"] = answer_comment['comment_message']
        #     user_answer_comments.append(answer)

        return render_template('user_page.html', user_details=user_details, user_questions=user_questions,
                               user_answers=user_answers, user_question_comments=user_question_comments,
                               user_answer_comments=user_answer_comments)
    else:
        return redirect(url_for("main"))


@app.route("/question/<question_id>")
def display_a_question(question_id):
    question = get_question(question_id)
    increase_view_number(question_id)
    question_tags = show_tags(question_id)
    answers = get_answer_by_question_id(question_id)
    question_comments = get_question_comments(question_id)
    return render_template('display_a_question.html',
                           question=question,
                           question_id=question_id,
                           answers=answers,
                           question_comments=question_comments,
                           question_tags=question_tags)


@app.route('/question/<question_id>/vote_up')
def vote_up_question(question_id):
    data = get_question_by_id(question_id)[0]
    user_id = data.get("user_id")
    reputation_up(user_id, 5)
    question_vote_up(question_id)
    return redirect("/")


@app.route('/question/<question_id>/vote_down')
def vote_down_question(question_id):
    data = get_question_by_id(question_id)[0]
    user_id = data.get("user_id")
    reputation_down(user_id, 2)
    question_vote_down(question_id)
    return redirect("/")


@app.route('/answer/<answer_id>/vote_up')
def vote_up_answer(answer_id):
    data = get_answer_by_comment_id(answer_id)[0]
    user_id = data.get("user_id")
    reputation_up(user_id, 10)
    answer_vote_up(answer_id)
    question_id = get_question_id(answer_id)['question_id']
    return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/answer/<answer_id>/vote_down')
def vote_down_answer(answer_id):
    data = get_answer_by_comment_id(answer_id)[0]
    user_id = data.get("user_id")
    reputation_down(user_id, 2)
    answer_vote_down(answer_id)
    question_id = get_question_id(answer_id)['question_id']
    return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/add_questions', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        if "username" in session:
            return render_template("add-question.html")
        else:
            return redirect("/login")
    if request.method == 'POST':
        image_name = upload()
        if "[302 FOUND]" in str(image_name):
            image_name = "None"
        new_question = {"view_number": 0,
                        "vote_number": 0,
                        "title": request.form.get("title"),
                        "message": request.form.get("message"),
                        "image": image_name,
                        "user_id": session.get('user_id')}
        add_a_question(new_question)
        return redirect("/")


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == "GET":
        question = get_question(question_id)
        return render_template("edit_question.html", question=question, question_id=question_id)
    if request.method == "POST":
        image_name = upload()
        if "[302 FOUND]" in str(image_name):
            image_name = "None"
        edited_data = request.form
        update_question(edited_data, question_id, image_name)
        return redirect(url_for('display_a_question', question_id=question_id))


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'GET':
        return render_template("delete_question.html", question_id=question_id)
    if request.method == 'POST':
        image_path = get_image_name_by_question_id(question_id)
        for answer in image_path:
            image_name = answer["image"]
        if os.path.exists(image_name):
            os.remove(image_name)
        else:
            print("The file does not exist")
        answer_ids = extract_answer_image_paths(question_id)
        for id in answer_ids:
            image_path = get_image_name_by_answer_id(id)
            for answer in image_path:
                image_name = answer["image"]
            if image_name == None:
                image_name = "None"
            if os.path.exists(image_name):
                os.remove(image_name)
            else:
                print("The file does not exist")
        delete_a_question(question_id)
        return redirect('/')


@app.route('/question/<int:question_id>/new_comment', methods=['GET', 'POST'])
def new_question_comment(question_id):
    if request.method == "GET":
        if "username" in session:
            return render_template("new_question_comment.html", question_id=str(question_id))
        else:
            return redirect("/login")
    elif request.method == "POST":
        new_comment = request.form["new_comment"]
        user_id = session.get('user_id')
        write_question_comment(question_id, new_comment, user_id)
        return redirect("/question/" + str(question_id))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_random_name():
   return str(random.randint(100000, 999999))


def upload():
    try:
        if request.method == 'POST':
                # if 'photo' not in request.files:
                #     flash('No file part')
                #     return redirect(request.url)
                file = request.files['photo']
                # if file.filename == '':
                #     flash('No selected file')
                #     return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    random_name = create_random_name()
                    filename = str(random_name)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #os.rename(UPLOAD_FOLDER + filename, UPLOAD_FOLDER + random_name()) # not sure if I even need these the problem is maybe elsewhere
                #file_name = random_name
        return f"static/uploads/{filename}"
    except UnboundLocalError:
        return "None"


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_add_answer(question_id):
    if request.method == 'GET':
        if "username" in session:
            return render_template("new_answer.html", question_id=question_id)
        else:
            return redirect("/login")
    if request.method == 'POST':
        image_name = upload()
        if "[302 FOUND]" in str(image_name):
            image_name = "None"
        new_answer = {'vote_number': 0,
                      'question_id': question_id,
                      'message': request.form.get('message'),
                      'image': image_name,
                      'accepted': False,
                      'user_id': session.get('user_id')}
        add_new_answer(new_answer)
        return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/answer/<answer_id>/delete', methods=["GET"])
def delete(answer_id):
    if request.method == 'GET':
        question_id = request.args.get('question_id')
        image_path = get_image_name_by_answer_id(answer_id)
        for answer in image_path:
            image_name = answer["image"]
        if os.path.exists(image_name):
            os.remove(image_name)
        else:
            print("The file does not exist")
        delete_answer(answer_id)
        return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'GET':
        question_id = request.args.get('question_id')
        answers = get_answer_by_id(answer_id, question_id)
        return render_template('edit_answer.html', answers=answers, answer_id=answer_id, question_id=question_id)
    if request.method == 'POST':
        image_name = upload()
        if "[302 FOUND]" in str(image_name):
            image_name = "None"
        question_id = request.args.get('question_id')
        new_answer = {'id': answer_id,
                      'question_id': question_id,
                      'message': request.form.get('message'),
                      'image': image_name}
        update_answer(new_answer)
        return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/delete_comment_conformation')
def are_you_sure():
    comment = request.args.get('comment')
    comment_id = request.args.get('comment_id')
    question_id = request.args.get('question_id')
    return render_template('delete_comment_confirmation.html',
                           comment=comment, question_id=question_id, comment_id=comment_id)


@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    question_id = request.args.get('question_id')
    delete_a_comment(comment_id)
    return redirect(url_for('display_a_question', question_id=question_id))


def extract_answer_image_paths(question_id):
    answer_paths = get_all_answers_image_path(question_id)
    return [(answer['id']) for answer in answer_paths]


@app.route('/answer/<answer_id>/new_comment', methods=['GET', 'POST'])
def new_answer_comment(answer_id):
    if request.method == "GET":
        if "username" in session:
            return render_template("new_answer_comment.html", answer_id=answer_id)
        else:
            return redirect("/login")
    elif request.method == "POST":
        new_comment = request.form["new_comment"]
        question_id = get_question_id(answer_id)['question_id']
        user_id = session.get('user_id')
        write_answer_comment(answer_id, new_comment, user_id)
        return redirect(url_for("display_a_question",question_id=question_id))




@app.route('/answer/show_answers')
def get_answers_comments():
    answer_id = request.args.get("answer_id")
    question_id = request.args.get("question_id")
    answer = get_answers(answer_id)
    question = get_question(question_id)
    answer_comments = get_answer_comments(answer_id)
    return render_template("answers.html", question_id=question_id, answer_id=answer_id, answer_comments=answer_comments, answer=answer, question=question)


@app.route('/tags')
def route_tags():
    tags_list = get_all_tags()
    return render_template('tag_list.html', tags_list=tags_list)


@app.route("/question/<question_id>/new-tag", methods=['GET', 'POST'])
def add_tag(question_id):
    if request.method == 'GET':
        return render_template("new_tag.html", question_id=question_id)
    if request.method == 'POST':
        new_tag = request.form.get('name')
        add_new_tag(new_tag, question_id)
        return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_a_tag(question_id, tag_id):
    delete_tag(tag_id)
    return redirect(url_for('display_a_question', question_id=question_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        registration_date = datetime.datetime.now()
        if not username:
            return 'Missing Username!', 400
        if not password:
            return 'Missing Password!', 400
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(hashed)
        add_new_user(username, hashed, registration_date, count_of_asked_questions=0, count_of_answers=0, count_of_comments=0, reputation=0)
        #return f'Welcome {email}'
        #return redirect(url_for('login'))
        return redirect(url_for('main'))
    return render_template('registration.html')


@app.route("/ASKM8")
def askm8():
    return render_template('projectinfo.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        if get_user_data(request.form["username"], request.form["password"]):
            username = request.form["username"]
            password = request.form["password"]
            user_data = get_user_data(username, password)
            user_password = user_data["password"]
            if bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8')):
                ID = get_user_id(username)
                session["user_id"] = ID['id']
                session["username"] = username
                return redirect("/")
            else:
                error = "Invalid login attempt!"
                return render_template("login.html", error=error)
        else:
            error = "Invalid login attempt!"
            return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect("/")

# #@app.route("/set_status")
# def set_status(user_id):
#     #user_id = session.get('user_id')
#     status_data = get_status_by_user_id(user_id)
#     status = status_data["accepted"]
#     if status:
#         set_status_by_user_id(user_id, False)
#     else:
#         set_status_by_user_id(user_id, True)


@app.route("/comment/<comment_id>/edit_comment", methods=["POST", "GET"])
def edit_comment(comment_id):
    if request.method == "GET":
        comment = get_comment_by_id(comment_id)
        return render_template("edit_comment.html", comment=comment, comment_id=comment_id)
    elif request.method == "POST":
        current_time = datedata
        updated_comment = {
            "message" : request.form.get("new-message"),
            "id" : comment_id,
            "submission_time": current_time}
        question_id = get_question_id_from_comment(comment_id)['question_id']
        increase_edit_number(comment_id)
        update_comments(updated_comment)
        if question_id:
            return redirect('/question/' + str(question_id))
        else:
            return redirect("/")
    return redirect(url_for("display_a_question", question_id=question_id))



@app.route("/user/<user_id>")
def user_page(user_id):
    pass


@app.route('/answer/<answer_id>/change_status', methods=["GET", "POST"])
def change_status(answer_id):
    if request.method == 'GET':
        question_id = request.args.get('question_id')
        user_id = session.get('user_id')
        answer_user_id = validate_user_by_answer_id(answer_id)
        check = answer_user_id['user_id']
        print(user_id)
        print(check)
        if user_id == check:
            status_data = get_status_by_answer_id(answer_id)
            status = status_data["accepted"]
            data = get_answer_by_comment_id(answer_id)[0]
            user_id = data.get("user_id")
            if status:
                set_status_by_answer_id(answer_id, False)
                reputation_down(user_id, 15)
            else:
                set_status_by_answer_id(answer_id, True)
                reputation_up(user_id, 15)
            return redirect(url_for("display_a_question", answer_id=answer_id, question_id=question_id))
        else:
            flash('You have no permission to mark this accepted.')
            print('bug')
            return redirect(url_for("display_a_question", question_id=question_id))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
