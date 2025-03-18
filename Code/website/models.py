from flask_bcrypt import bcrypt
from sqlalchemy import DateTime
from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import json


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(100))
    xp = db.Column(db.Text, nullable=False)

    def __init__(self, email, password, role='user', xp={}):
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.xp = json.dumps(xp)

    def check_pass(self, password):
        return check_password_hash(self.password, password)


class Subject(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    chapters = db.relationship('Chapter', backref='subject', lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.chapters = []

    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "chapters": [chapter.toJson() for chapter in self.chapters]
        }


class Chapter(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer(), db.ForeignKey(
        'subject.id'), nullable=False)
    questions = db.relationship('Questions', backref='chapter', lazy=True)

    def __init__(self, name, description, subject_id):
        self.name = name
        self.description = description
        self.subject_id = subject_id

    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "questions": [ques.toJson() for ques in self.questions]
        }


class Questions(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    question = db.Column(db.String(100), nullable=False)
    options = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    chapter_id = db.Column(db.Integer(), db.ForeignKey(
        'chapter.id'), nullable=False)

    def __init__(self, question, options, answer, chapter_id):
        self.question = question
        self.options = json.dumps(options)
        self.answer = answer
        self.chapter_id = chapter_id

    def toJson(self):
        return {
            "id": self.id,
            "question": self.question,
            "options": json.loads(self.options),
            "answer": self.answer,
            "chapter_id": self.chapter_id
        }


class Quiz(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    chapter_id = db.Column(db.Integer(), db.ForeignKey(
        'chapter.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time_duration = db.Column(db.Integer(), nullable=False)

    def __init__(self, chapter_id, date, time_duration):
        self.chapter_id = chapter_id
        self.date = date
        self.time_duration = time_duration

    def toJson(self):
        return {
            "id": self.id,
            "chapter_id": self.chapter_id,
            "date": self.date,
            "time_duration": self.time_duration
        }


class Scores(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id'), nullable=False)
    quiz_id = db.Column(db.Integer(), db.ForeignKey(
        'quiz.id'), nullable=False)
    attempt_timestamp = db.Column(db.DateTime)
    score = db.Column(db.Integer(), nullable=False)

    def __init__(self, user_id, quiz_id, attempt_timestamp, score):
        self.user_id = user_id
        self.quiz_id = quiz_id
        self.attempt_timestamp = attempt_timestamp
        self.score = score

    def toJson(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "quiz_id": self.quiz_id,
            "attempt_timestamp": self.attempt_timestamp,
            "score": self.score
        }
