from flask_bcrypt import bcrypt
import datetime
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
    xp = db.Column(db.Integer(), nullable=False)


class Chapter(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    xp = db.Column(db.Integer(), nullable=False)
    subject_id = db.Column(db.Integer(), db.ForeignKey(
        'subject.id'), nullable=False)


class Questions(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    question = db.Column(db.String(100), nullable=False)
    options = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    chapter_id = db.Column(db.Integer(), db.ForeignKey(
        'chapter.id'), nullable=False)
    chapter = db.relationship('Chapter', backref='questions', lazy=True)


class Quiz(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    chapter_id = db.Column(db.Integer(), db.ForeignKey(
        'chapter.id'), nullable=False)
    date = db.Column(db.DateTime)
    time_duration = db.Column(db.Datetime, nullable=False)


class Scores(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id'), nullable=False)
    quiz_id = db.Column(db.Integer(), db.ForeignKey(
        'quiz.id'), nullable=False)
    attempt_timestamp = db.Column(db.DateTime)
    score = db.Column(db.Integer(), nullable=False)
