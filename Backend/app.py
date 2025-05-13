from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
from functools import wraps
import jwt
import os
import speech_recognition as sr
from werkzeug.security import generate_password_hash, check_password_hash
from Levenshtein import ratio as levenshtein_ratio
from sqlalchemy.exc import SQLAlchemyError
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure CORS properly
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "http://localhost:2023",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Authorization", "Content-Type"],
        "supports_credentials": False
    }
})


# Database Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/language_app?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Initialize database
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(190), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Progress(db.Model):
    __tablename__ = 'progress'
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    word = db.Column(db.String(50), nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ExpectedText(db.Model):
    __tablename__ = 'expected_texts'
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    phonetic = db.Column(db.String(255))
    difficulty = db.Column(db.String(50), default='medium')

# Authentication Middleware
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                raise ValueError("User not found")
            return f(current_user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except (jwt.InvalidTokenError, ValueError) as e:
            return jsonify({'error': 'Invalid token!'}), 401
    
    return decorator

# Helper Functions
def save_audio(file):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    filename = f"{datetime.now().timestamp()}.wav"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return file_path

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the AI English Learning Platform API!"}), 200

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'User already exists'}), 409
        
        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            email=data['email'],
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        
        if user and check_password_hash(user.password, data['password']):
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, app.config['SECRET_KEY'])
            return jsonify({'token': token}), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/evaluate_pronunciation', methods=['GET'])
@token_required
def evaluate_pronunciation(current_user):
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file uploaded'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        audio_path = save_audio(audio_file)
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            recognized_text = recognizer.recognize_google(audio_data)
        
        expected_entry = ExpectedText.query.order_by(db.func.random()).first()
        expected_text = expected_entry.text
        
        accuracy = levenshtein_ratio(
            expected_text.lower(), 
            recognized_text.lower()
        ) * 100
        
        progress_entry = Progress(
            user_id=current_user.id,
            word=expected_entry.text,
            accuracy=accuracy
        )
        db.session.add(progress_entry)
        db.session.commit()
        
        return jsonify({
            'expected_text': expected_text,
            'recognized_text': recognized_text,
            'accuracy': round(accuracy, 2),
            'feedback': 'Good pronunciation!' if accuracy >= 70 else 'Needs improvement'
        }), 200
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 400
    except Exception as e:
        logger.error(f"Evaluation error: {str(e)}")
        return jsonify({'error': 'Evaluation failed'}), 500
    finally:
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)

@app.route('/api/user_stats', methods=['GET'])
@token_required
def user_stats(current_user):
    try:
        total_evaluations = Progress.query.filter_by(user_id=current_user.id).count()
        
        average_accuracy = db.session.query(
            db.func.round(db.func.avg(Progress.accuracy), 2)
        ).filter_by(user_id=current_user.id).scalar() or 0
        
        last_evaluation = Progress.query.filter_by(
            user_id=current_user.id
        ).order_by(
            Progress.timestamp.desc()
        ).first()
        
        response_data = {
            "totalEvaluations": total_evaluations,
            "averageAccuracy": float(average_accuracy),
            "lastEvaluation": last_evaluation.timestamp.isoformat() if last_evaluation else None
        }
        
        return jsonify(response_data)
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Initialize Database
def initialize_data():
    with app.app_context():
        db.create_all()
        
        if not ExpectedText.query.first():
            texts = [
                ("The quick brown fox jumps over the lazy dog", "ðə kwɪk braʊn fɑːks ʤʌmps ˈoʊvər ðə ˈleɪzi dɔːɡ"),
                ("She sells seashells by the seashore", "ʃiː sɛlz ˈsiːʃɛlz baɪ ðə ˈsiːʃɔːr"),
                ("How can a clam cram in a clean cream can?", "haʊ kæn ə klæm kræm ɪn ə kliːn kriːm kæn")
            ]
            for text, phonetic in texts:
                db.session.add(ExpectedText(
                    text=text,
                    phonetic=phonetic,
                    difficulty='medium'
                ))
            db.session.commit()

if __name__ == '__main__':
    initialize_data()
    app.run(host='0.0.0.0', port=5000, debug=True)