from flask_bcrypt import bcrypt
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


class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    time_required = db.Column(db.Integer, nullable=True)

    def __init__(self, name, description, price, time_required=0):
        self.name = name
        self.description = description
        self.price = price
        self.time_required = time_required


class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey(
        'services.id'), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    date_of_request = db.Column(db.DateTime, nullable=False)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    remarks = db.Column(db.Text, nullable=True)

    def __init__(self, customer_id, professional_id, service_id, status, date_of_request, date_of_completion=None, remarks=None):
        self.customer_id = customer_id
        self.professional_id = professional_id
        self.service_id = service_id
        self.status = status
        self.date_of_request = date_of_request
        self.date_of_completion = date_of_completion
        self.remarks = remarks
