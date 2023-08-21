from flask import render_template, flash, redirect, url_for,request,jsonify
from app import app,db
from app.forms import LoginForm,RegistrationForm,RecognitionForm,UploadDocumentForm,RegistrationForm2,ProfileForm
from flask_login import current_user, login_user,logout_user,login_required
from app.models import User,Reception
from werkzeug.urls import url_parse
from io import BytesIO
from PIL import Image
import base64
import cv2
import dlib
import numpy as np
face_detector = dlib.get_frontal_face_detector()
import face_recognition
from datetime import datetime
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
import pytesseract
pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
from PIL import Image
import matplotlib.pyplot as plt
import io 

""" @app.route('/')
@app.route('/index')
@login_required
def index():
    users = User.query.all()
    return render_template("index.html", title='Home Page', user=users) """

""" @app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form) """



""" @app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        name = form.name.data
        surname = form.surname.data
        password = form.password.data

        # Base64 encoded image data received from the form
        picture_data_base64 = form.picture.data

        # Decode the base64 encoded image data to bytes
        try:
            # Remove the data URI prefix if it exists
            if picture_data_base64.startswith('data:image'):
                _, picture_data_base64 = picture_data_base64.split(',', 1)
            
            picture_data = picture_data_base64.encode('utf-8')
            picture_data = base64.b64decode(picture_data)
        except Exception as e:
            flash('Error decoding the picture.')
            return redirect(url_for('register'))

        # Save the new user to the database
        user = User(username=username, email=email, name=name, surname=surname, picture=picture_data)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form) """

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm2()
    if form.validate_on_submit():
        """ name = form.name.data
        surname = form.surname.data
        citizenship = form.citizenship.data """
        
        picture_data_base64 = form.picture.data
        try:
            if picture_data_base64.startswith('data:image'):
                _, picture_data_base64 = picture_data_base64.split(',', 1)
            
            picture_data = picture_data_base64.encode('utf-8')
            picture_data = base64.b64decode(picture_data)
        except Exception as e:
            flash('Error decoding the picture.')
            return redirect(url_for('register'))

        #user = User(name=name, surname=surname, picture=picture_data,citizenship=citizenship)
        user = User(picture=picture_data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('profile', user_id=user.id))
    return render_template('register.html', title='Register', form=form)

@app.route('/')
def index():
    return redirect('/welcome')

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('welcome'))

@app.route('/recognition', methods=['GET', 'POST'])
def recognition():
    form = RecognitionForm()
    if form.validate_on_submit():
        picture_data_base64 = form.picture.data
        if picture_data_base64:
            image_bytes = base64.b64decode(picture_data_base64.split(',')[1])
            img = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_recognition.face_locations(gray_img)
            if len(faces) > 0:
                face_encoding_to_check = face_recognition.face_encodings(img, faces)[0]
                users = User.query.all()
                for user in users:
                    if user.picture is None:
                        continue

                    user_image = np.frombuffer(user.picture, dtype=np.uint8)
                    user_img = cv2.imdecode(user_image, cv2.IMREAD_COLOR)

                    user_face_encoding = face_recognition.face_encodings(user_img)

                    if user_face_encoding is not None and len(user_face_encoding) > 0:
                        is_match = face_recognition.compare_faces(user_face_encoding, face_encoding_to_check)
                        if any(is_match):
                            today = datetime.now().date()
                            existing_entry = Reception.query.filter_by(user_id=user.id, entry_date=today).first()

                            if existing_entry:
                                formatted_time = existing_entry.entry_time.strftime('%H:%M:%S')
                                flash(f'You have already been registered today at {formatted_time}.')
                                return redirect(url_for('reception'))
                            else:
                                 flash(f'Welcome {user.name} {user.surname}')

                            recognition_data = Reception(
                                user_id=user.id,
                                entry_date=today,
                                entry_time=datetime.now().time(),  
                            )
                            db.session.add(recognition_data)
                            db.session.commit()

                            _, img_encoded = cv2.imencode('.jpg', img)
                            img_base64 = base64.b64encode(img_encoded).decode('utf-8')

                            return redirect(url_for('reception', recognition_data=recognition_data))

                return redirect(url_for('register'))

    return render_template('recognition.html', form=form)

@app.route('/upload_documents/<int:user_id>', methods=['POST'])
def upload_documents(user_id):
    form = UploadDocumentForm()
    user = User.query.get(user_id)

    if user is None:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        front_document_file = form.front_document.data
        back_document_file = form.back_document.data
        if front_document_file:
            filename = secure_filename(front_document_file.filename)
            front_document_data = front_document_file.read()
            user.front_document = front_document_data

        if back_document_file:
            filename = secure_filename(back_document_file.filename)
            back_document_data = back_document_file.read()
            user.back_document = back_document_data   
        db.session.commit()
        flash('Images uploaded and saved successfully!')

    front_document_blob = user.front_document
    back_document_blob = user.back_document


    image_front = Image.open(io.BytesIO(front_document_blob))
    image_cv2 = cv2.cvtColor(np.array(image_front), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
    text1 = pytesseract.image_to_data(threshed, output_type='data.frame')
    text2 = pytesseract.image_to_string(threshed, lang="hrv")
    text = text1[text1.conf != -1]
    lines = text.groupby('block_num')['text'].apply(list)
    conf = text.groupby(['block_num'])['conf'].mean()

        
    for i in range(len(lines)):
            print("level prednja:", i, ": ", lines.iloc[i])
        
    try:
        user.name = lines.iloc[14][0]
    except IndexError:
        user.name = ""

    try:
        user.surname = lines.iloc[12][0]
    except IndexError:
        user.surname = ""

    try:
        user.sex = lines.iloc[14][3]
    except IndexError:
        user.sex = ""

    try:
        user.identity_card_number = lines.iloc[5][0]
    except IndexError:
        user.identity_card_number = ""

    try:
        input_string = lines.iloc[15][1]
        cleaned_string = input_string.translate(str.maketrans('', '', '©.'))
        user.date_of_birth = datetime.strptime(cleaned_string, '%d%m%Y').date() if len(cleaned_string) == 8 else None
    except IndexError:
        user.date_of_birth = None

    try:
        user.country = lines.iloc[8][2]
    except IndexError:
        user.country = ""


    image_back = Image.open(io.BytesIO(back_document_blob))
    image_cv2_back = cv2.cvtColor(np.array(image_back), cv2.COLOR_RGB2BGR)
    gray_back = cv2.cvtColor(image_cv2_back, cv2.COLOR_BGR2GRAY)
    th_back, threshed_back = cv2.threshold(gray_back, 127, 255, cv2.THRESH_TRUNC)
    text1_back = pytesseract.image_to_data(threshed_back, output_type='data.frame')
    text2_back = pytesseract.image_to_string(threshed_back, lang="hrv")
    text_back = text1_back[text1_back.conf != -1]
    lines_back = text_back.groupby('block_num')['text'].apply(list)
    conf_back = text_back.groupby(['block_num'])['conf'].mean()

    for i in range(len(lines_back)):
        print("level stražnja:", i, ": ", lines_back.iloc[i])
        
    try:
        residence2 = lines_back.iloc[0][2]
        user.residence = lines_back.iloc[0][1] + " " + residence2
    except IndexError:
        user.residence = ""
    try:
        user.oib = lines_back.iloc[6][0]
    except IndexError:
        user.oib = ""


    db.session.commit()


    return redirect(url_for('profile', user_id=user.id))


@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    form = UploadDocumentForm()
    Profileform = ProfileForm()
    user = User.query.get(user_id)

    if user is None:
        return redirect(url_for('index'))

    def get_base64_image(image_data):
        if image_data is not None:
            base64_data = base64.b64encode(image_data).decode('utf-8')
            return f"data:image/jpeg;base64,{base64_data}"
        return None
    
    if request.method == 'GET':
        Profileform.surname.data = user.surname
        Profileform.name.data = user.name
        Profileform.country.data = user.country
        Profileform.residence.data = user.residence
        Profileform.date_of_birth.data = user.date_of_birth
        Profileform.oib.data = user.oib

    if Profileform.validate_on_submit():
        user.surname = Profileform.surname.data
        user.name = Profileform.name.data
        user.country = Profileform.country.data
        user.residence = Profileform.residence.data
        user.date_of_birth = Profileform.date_of_birth.data
        user.oib = Profileform.oib.data
        print( Profileform.surname.data,Profileform.name.data,Profileform.country.data,Profileform.residence.data,Profileform.date_of_birth.data,Profileform.oib.data  )
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('profile', user_id=user.id))
    

    base64_image = get_base64_image(user.picture)
    front_document = get_base64_image(user.front_document)
    back_document = get_base64_image(user.back_document)

    
    return render_template('profile.html', user=user, base64_image=base64_image, form=form, front_document=front_document, back_document=back_document,Profileform=Profileform)

@app.route('/reception', methods=['GET'])
def reception():
    selected_date_str = request.args.get('date')
    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        entries = Reception.query.filter(Reception.entry_date == selected_date).options(joinedload(Reception.user)).all()
    else:
        entries = Reception.query.all()
    today_date = datetime.now().strftime('%d-%m-%Y')

    return render_template('reception.html', entries=entries, today_date=today_date)

""" @app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) """

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')