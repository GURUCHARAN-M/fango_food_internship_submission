from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("email")
app.config['MAIL_PASSWORD'] = os.getenv("pass")

mail = Mail(app)

def generate_response(query):
    return f"You asked: {query}. This is the system's response."

@app.route('/send', methods=['POST'])
def send():
    try:
        data = request.json
        query = data.get('query')
        email = data.get('email')
        if not query or not email:
            return jsonify({"error": "Query and recipient email are required"}), 400
        response = generate_response(query)
        email_body = f"Query: {query}\nResponse: {response}"
        msg = Message(
            subject="Response to Your Query",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email],
            body=email_body
        )
        mail.send(msg)
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
