import os
import json
import time
import logging
import threading
import pythoncom
import win32com.client as win32
from flask import Flask, render_template, request, jsonify
from validation import validate_application

app = Flask(__name__)

# Set up logging
log_file_path = os.path.join(os.getcwd(), 'logs', 'validation.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

validation_status = {'status': 'Not Started', 'results': []}

def send_email(subject, validation_results):
    email_body = (
        "<html>"
        "<body style='font-family: Arial, sans-serif;'>"
        "<p>Hi Team,</p>"
        "<p>Please find the validation result of <strong>FPA IT Application</strong>:</p>"
        "<pre style='font-size: 14px; color: #333;'>"
    )

    for result, status in validation_results:
        email_body += f"{result}\n"

    email_body += "</pre>"
    if all([status == "Success" for result, status in validation_results]):
        email_body += "<p style='font-size: 18px; color: green;'><strong>Validation Successful</strong></p>"
    else:
        email_body += "<p style='font-size: 18px; color: red;'><strong>Validation Failed</strong></p>"
    email_body += (
        "<p>Best regards,</p>"
        "<p><strong>Your Name</strong><br>"
        "Your Position<br>"
        "Your Contact Information</p>"
        "</body>"
        "</html>"
    )

    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'Pratik_Bhongade@keybank.com'  # Replace with the recipient email addresses
    mail.Subject = subject
    mail.HTMLBody = email_body
    mail.Attachments.Add(log_file_path)  # Attach the log file
    mail.Send()
    pythoncom.CoUninitialize()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_validation', methods=['POST'])
def start_validation():
    data = request.json
    environment = data.get('environment')
    validation_status['status'] = 'Running'
    validation_status['results'] = []

    def validate_environment():
        results, success = validate_application(environment)
        validation_status['status'] = 'Completed' if success else 'Failed'
        validation_status['results'] = results
        subject = f"FPA {environment.upper()} Environment Validation Results"
        send_email(subject, results)

    thread = threading.Thread(target=validate_environment)
    thread.start()
    return jsonify({"message": "Validation started"}), 202

@app.route('/status')
def status():
    return jsonify(validation_status)

if __name__ == '__main__':
    app.run(debug=True)
