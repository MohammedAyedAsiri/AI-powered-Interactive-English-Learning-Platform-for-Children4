from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # علاقة مع الجداول الأخرى
    evaluations = relationship('Evaluation', backref='user', lazy=True)
    sessions = relationship('Session', backref='user', lazy=True)
    feedbacks = relationship('Feedback', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Word(db.Model):
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True)
    text = Column(String(100), nullable=False)

    # علاقة مع الجداول الأخرى
    evaluations = relationship('Evaluation', backref='word', lazy=True)
    words_in_context = relationship('WordInContext', backref='word', lazy=True)

class Evaluation(db.Model):
    __tablename__ = 'evaluations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    word_id = Column(Integer, ForeignKey('word.id'), nullable=False)
    recognized_text = Column(String(255))
    accuracy = Column(Float, nullable=False)

    # يمكن أن تضيف خاصية لتعريف الوقت
    timestamp = Column(db.DateTime, server_default=db.func.now())

class Session(db.Model):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    login_time = Column(db.DateTime, server_default=db.func.now())
    logout_time = Column(db.DateTime)

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    evaluation_id = Column(Integer, ForeignKey('evaluations.id'), nullable=False)
    comment = Column(Text)

    created_at = Column(db.DateTime, server_default=db.func.now())

class WordInContext(db.Model):
    __tablename__ = 'words_in_context'

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('word.id'), nullable=False)
    context = Column(Text)