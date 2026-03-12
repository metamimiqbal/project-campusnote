from datetime import datetime
from campusnote import db
from flask_login import UserMixin

class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    departments = db.relationship('Department', backref='university', lazy=True)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    years = db.relationship('Year', backref='department', lazy=True)

    __table_args__ = (db.UniqueConstraint('name', 'university_id'),)


class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(20), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    semesters = db.relationship('Semester', backref='year', lazy=True)

    __table_args__ = (db.UniqueConstraint('label', 'department_id'),)


class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(20), nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'), nullable=False)
    subjects = db.relationship('Subject', backref='semester', lazy=True)

    __table_args__ = (db.UniqueConstraint('label', 'year_id'),)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    notes = db.relationship('Note', backref='subject', lazy=True)

    __table_args__ = (db.UniqueConstraint('name', 'semester_id'),)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # store hashed, never plaintext
    profile_pic = db.Column(db.String(200), default='default.jpg')
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.relationship('Note', backref='uploader', lazy=True)
    
        

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(300), nullable=False)  
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)  # e.g. 1-5
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    
    # Prevent one user rating the same note twice
    __table_args__ = (db.UniqueConstraint('user_id', 'note_id'),)
