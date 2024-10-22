from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from reportlab.lib.pagesizes import letter
from flask_cors import CORS
from reportlab.pdfgen import canvas
from pymongo import MongoClient  # MongoDB driver
import os
import io
from bson import ObjectId

app = Flask(__name__)
app.secret_key = '5f62c34db0967ddf3a06a8c82a787d8009bb4aed69511342'  # Required for session management and flash messages

# MongoDB connection setup
MONGO_URI = "mongodb+srv://shifannagarji26:Shifan12345@cluster0.arvthjn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['submissions']  # Replace with your MongoDB database name
submissions_collection = db['submissions']  # Replace with your collection name

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Replace with your Gmail address
app.config['MAIL_PASSWORD'] = 'your_email_password'    # Replace with your Gmail password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'  # Same as above
mail = Mail(app)

# Directory where uploaded files will be saved
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# Route to handle form submission
@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        hours = request.form.get('hours')
        pages = request.form.get('pages')
        education = request.form.get('education')

        # Get the uploaded PDF file and payment screenshot
        pdf_file = request.files.get('pdf')
        payment_screenshot = request.files.get('payment')

        if pdf_file and pdf_file.filename != '':
            pdf_filename = secure_filename(pdf_file.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
            pdf_file.save(pdf_path)
        else:
            return jsonify({'success': False, 'message': 'PDF file is required'}), 400

        if payment_screenshot and payment_screenshot.filename != '':
            payment_filename = secure_filename(payment_screenshot.filename)
            payment_path = os.path.join(app.config['UPLOAD_FOLDER'], payment_filename)
            payment_screenshot.save(payment_path)
        else:
            return jsonify({'success': False, 'message': 'Payment screenshot is required'}), 400

        # Insert the data into the MongoDB collection and get the inserted document ID
        result = submissions_collection.insert_one({
            'username': username,
            'email': email,
            'mobile': mobile,
            'hours': hours,
            'pages': pages,
            'education': education,
            'pdf_path': pdf_path,
            'payment_path': payment_path
        })
        submission_id = str(result.inserted_id)  # Convert ObjectId to string

        return jsonify({'success': True, 'message': 'Form submitted successfully!', 'submission_id': submission_id}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to fetch submissions data
@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    try:
        submissions = list(submissions_collection.find({}))
        # Convert MongoDB ObjectId to string for JSON serialization
        for submission in submissions:
            submission['_id'] = str(submission['_id'])
        return jsonify(submissions), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == "__main__":
 app.run(port=3000, debug=True)

