# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:2023/language_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models (if they're not imported from models.py)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(190), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class PronunciationScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Pronunciation evaluation placeholder function
def evaluate_pronunciation(audio):
    # Here, you would implement your audio processing logic; returning a fixed score for demonstration
    return 0.0  # Placeholder score

@app.route('/api/evaluate_pronunciation', methods=['POST'])
def evaluate_pronunciation_route():
    audio_file = request.files.get('audio')
    user_id = request.form.get('user_id')  # Get user ID from form data

    if not audio_file or not user_id:
        return jsonify({'error': 'Audio file and user ID are required'}), 400

    score = evaluate_pronunciation(audio_file)  # Call the evaluation function
    pronunciation_score = PronunciationScore(user_id=user_id, score=score)
    
    db.session.add(pronunciation_score)  # Save the score to the database
    db.session.commit()

    return jsonify({
        'message': 'Evaluation completed',
        'score': score
    }), 200

# User Registration and Login routes here...

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)