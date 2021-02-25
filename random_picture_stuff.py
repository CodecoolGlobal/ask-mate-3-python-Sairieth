# def upload_pictures():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['PICTURE_UPLOADS'], filename))


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route("/picture", methods=["GET", "POST"])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'picture' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['picture']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['PICTURE_UPLOADS'], filename))
#     return redirect(url_for('add_question'))