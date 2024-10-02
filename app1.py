from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from reportlab.lib.pagesizes import letter
from flask_cors import CORS
from reportlab.pdfgen import canvas
from pymongo import MongoClient  # MongoDB driver
import os
import io

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
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        hours = request.form['hours']
        pages = request.form['pages']
        education = request.form['education']
        payment = request.form['payment']  # Assuming payment amount is sent with form data

        # Get file data
        if 'pdf' not in request.files:
            return jsonify({'success': False, 'message': 'No file part in the request'}), 400

        pdf = request.files['pdf']
        if pdf.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400

        # Validate the file type
        if not pdf.filename.endswith('.pdf'):
            return jsonify({'success': False, 'message': 'Only PDF files are allowed'}), 400

        # Secure the filename and save the file
        filename = secure_filename(pdf.filename)
        pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Insert data into MongoDB
        submission = {
            "username": username,
            "email": email,
            "mobile": mobile,
            "pdf": filename,
            "hours": hours,
            "pages": pages,
            "education": education,
            "payment": payment
        }
        submissions_collection.insert_one(submission)

        return jsonify({'success': True, 'message': 'Form submitted successfully!'}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Error saving to database'}), 500

# Route to generate PDF receipt
@app.route('/generate_receipt/<submission_id>', methods=['GET'])
def generate_receipt(submission_id):
    try:
        # Fetch submission data from MongoDB
        submission = submissions_collection.find_one({"_id": submission_id})
        if not submission:
            return jsonify({'success': False, 'message': 'Submission not found'}), 404

        username = submission['username']
        email = submission['email']
        mobile = submission['mobile']
        payment = submission['payment']

        # Create a PDF in memory
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.drawString(100, 750, f"Receipt for {username}")
        c.drawString(100, 730, f"Email: {email}")
        c.drawString(100, 710, f"Phone: {mobile}")
        c.drawString(100, 690, f"Payment: ${payment}")
        c.drawString(100, 670, f"Submission ID: {submission_id}")
        c.drawString(100, 650, "Thank you for your submission!")
        c.showPage()
        c.save()

        pdf_buffer.seek(0)

        return send_file(pdf_buffer, as_attachment=True, download_name=f"receipt_{submission_id}.pdf", mimetype='application/pdf')

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Error generating receipt'}), 500
if __name__ == "__main__":
 app.run(port=3000, debug=True)

