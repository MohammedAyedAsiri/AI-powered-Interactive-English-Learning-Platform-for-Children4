from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    evaluations = db.relationship('Evaluation', backref='user', lazy=True)
    sessions = db.relationship('Session', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)

class Word(db.Model):
    __tablename__ = 'word'
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    phonetic = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(50), default='medium')
    
    # Relationships
    evaluations = db.relationship('Evaluation', backref='word', lazy=True)
    contexts = db.relationship('WordContext', backref='word', lazy=True)

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    recognized_text = db.Column(db.String(255))
    accuracy = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    feedback = db.relationship('Feedback', backref='evaluation', uselist=False)

class Session(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime)
    ip_address = db.Column(db.String(45))

class Feedback(db.Model):
    __tablename__ = 'feedback'
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluations.id'), nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WordContext(db.Model):
    __tablename__ = 'words_in_context'
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    context = db.Column(db.Text, nullable=False)
    example_audio = db.Column(db.String(255))

class ExpectedText(db.Model):
    __tablename__ = 'expected_texts'
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    phonetic = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), default='general')
    difficulty_score = db.Column(db.Float, default=1.0)


def initialize_data():

    sample_words = [
        ("The quick brown fox", "ðə kwɪk braʊn fɑːks"),
        ("Jump over the lazy dog", "ʤʌmp ˈoʊvər ðə ˈleɪzi dɔːɡ"),
        ("She sells seashells", "ʃiː sɛlz ˈsiːʃɛlz"),
        ("By the seashore", "baɪ ðə ˈsiːʃɔːr")
    ]
    
    for text, phonetic in sample_words:
        if not Word.query.filter_by(text=text).first():
            word = Word(
                text=text,
                phonetic=phonetic,
                difficulty='medium'
            )
            db.session.add(word)
    
    db.session.commit()