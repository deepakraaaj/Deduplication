import os
import numpy as np
import scipy.io.wavfile
import boto3
from flask import Flask, jsonify, request, redirect, render_template, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from utils.audio_processing import proposed_model
from models.user import User
from utils.database import get_db_connection, initialize_db, insert_user, get_user_by_credentials, get_user_by_id, get_all_subsets

# Flask app configuration
app = Flask(__name__)
app.config.from_object('config.Config')

# AWS S3 configuration
s3 = boto3.client('s3')

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database setup
conn = get_db_connection()
cursor = conn.cursor()
initialize_db(cursor)

@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_id(cursor, user_id)
    if user_data:
        return User(id=user_data[0], username=user_data[1], password=user_data[2])
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        insert_user(cursor, username, password)
        flash('Registration successful! Please log in.', 'success')
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_credentials(cursor, username, password)
        if user:
            login_user(User(id=user[0], username=user[1], password=user[2]))
            return redirect('/')
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            proposed_model(current_user.id, filename, filepath, cursor, s3, app.config['S3_BUCKET'])
            return redirect('/')
    return render_template('upload.html')

@app.route('/results')
@login_required
def results():
    formatted_data = get_formatted_data_from_db(cursor)
    return jsonify({"duplicates": formatted_data})

def get_formatted_data_from_db(cursor):
    subset_list = get_all_subsets(cursor)
    formatted_data = []
    for item in subset_list:
        user, filename, master, rate, start, end = item[1], item[2], item[3], item[4], item[5], item[6]
        description = f"Segment from {start}s to {end}s in the uploaded file matches with segment from {start}s to {end}s in the master file"
        formatted_data.append({
            "description": description,
            "master_start_time": start,
            "master_end_time": end,
            "master_file": master
        })
    return formatted_data

if __name__ == '__main__':
    app.run(debug=True)
