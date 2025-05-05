#from app import db
from extensions import db


class Freelancer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    skills = db.Column(db.String(200))
    availability = db.Column(db.String(50))

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    jobs = db.relationship('Job', backref='client_ref', cascade="all, delete-orphan")


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(300))
    pay_rate = db.Column(db.String(50))
    date_posted = db.Column(db.Date)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
