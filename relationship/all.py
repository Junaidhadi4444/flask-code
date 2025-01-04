# all relationship 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/all_RS'  # Change the URI as needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# One-to-One Relationship
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    profile = db.relationship('Profile', back_populates='user', uselist=False)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='profile')

# One-to-Many Relationship
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    books = db.relationship('Book', backref='author', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

# Many-to-Many Relationship
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    courses = db.relationship('Course', secondary='student_course', back_populates='students')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    students = db.relationship('Student', secondary='student_course', back_populates='courses')

class StudentCourse(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)

@app.route('/')
def index():
    # Get the first author, or handle the case where no author exists
    author = Author.query.first()

    if author is None:
        return 'No authors found in the database.'

    books = author.books  # Access books directly as it's a relationship

    student = Student.query.first()  # Get the first student
    courses = student.courses  # Get all courses the student is enrolled in

    return f'Author: {author.name}, Books: {[book.title for book in books]}<br>' \
           f'Student: {student.name}, Courses: {[course.title for course in courses]}'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
