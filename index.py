# Entering Virtual Environment and starting Git Bash
# source virt/Scripts/activate
# export FLASK_ENV=development
# export FLASK_APP=main.py

from flask import request, Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Create a flask instance
app = Flask(__name__)

# Add MySQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Bitrux&777@localhost/users'
# Secret Key
app.config['SECRET_KEY'] = "NonProductionWeb"
# Initialize Database
db = SQLAlchemy(app)

# Update 2 year old code lol. Resolve Flask 3.0 issue
app.app_context().push()

# Development use - migrate for new schemas
migrate = Migrate(app, db)

# Create Database Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    type = db.Column(db.String(16), nullable=False)
    feed = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create a route decorator
@app.route('/')
def index():
    return render_template('index.html')

# Create a feedback form page
@app.route('/user/add', methods=['GET', 'POST'])
def add_feedback():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        type = request.form.get('type')
        feed = request.form.get('feed')

        user = Users.query.filter_by(email=email).first()
        if len(email) < 4:
            flash('Invalid Email Address.')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.')
        elif len(type) < 3:
            flash('Invalid feedback type')
        elif len(feed) < 10:
            flash('Kindly provide a feedback comment more than 10 character(s)')
        elif user:
            flash("This user has already submitted a form.")
        else:
            user = Users(name=name, 
            email=email,
            type=type,
            feed=feed)

            db.session.add(user)
            db.session.commit()
            flash("Feedback submitted!")
    our_users = Users.query.order_by(Users.date_added)

    return render_template("add_feedback.html", our_users=our_users)

# Create a feedbacks view page
@app.route('/feedbacks', methods=['GET'])
def feedbacks():
    # Query feedbacks from the database
    feedbacks = Users.query.order_by(Users.date_added)
    return render_template('feedbacks.html', feedbacks=feedbacks)


# Create custom error pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500