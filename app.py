from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pandas as pd
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_BINDS'] = {'contact': 'sqlite:///contact.db', 'register': 'sqlite:///register.db'}
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Contact(db.Model):
    __bind_key__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    query = db.Column(db.Text, nullable=False)

class Register(db.Model):
    __bind_key__ = 'register'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Image = db.Column(db.String(120), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Category = db.Column(db.String(50), nullable=False)
    GoToFile = db.Column(db.String(120), nullable=False)

def save_to_excel(data, excel_file_path):
    if os.path.exists(excel_file_path):
        df = pd.read_excel(excel_file_path)
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    else:
        df = pd.DataFrame(data)

    df.to_excel(excel_file_path, index=False)

def read_excel_data(excel_file_path):
    if os.path.exists(excel_file_path):
        df = pd.read_excel(excel_file_path)
        return df.to_dict(orient='records')
    else:
        return []

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/mainpage.html')
def mainpage():
    return render_template('mainpage.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/')
def index():
    return render_template('mainpage.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    name = request.form.get('name')
    email = request.form.get('email')
    query = request.form.get('query')

    contact_info = Contact(name=name, email=email, query=query)

    db.session.add(contact_info)
    db.session.commit()

    # Save to Excel
    excel_file_path = os.path.join(app.instance_path, 'contact.xlsx')
    data = {'Name': [name], 'Email': [email], 'Query': [query]}
    save_to_excel(data, excel_file_path)

    return render_template('contact.html', sent=True)

@app.route('/model.html')
def model():
    excel_file_path = os.path.join(app.instance_path, 'model.xlsx')  
    products = read_excel_data(excel_file_path)
    return render_template('model.html', products=products)

@app.route('/project.html')
def project():
    excel_file_path = os.path.join(app.instance_path, 'project.xlsx')  
    products = read_excel_data(excel_file_path)
    return render_template('project.html', products=products)

@app.route('/process_register', methods=['POST'])
def process_register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    user = Register(username=username, email=email, password_hash=bcrypt.generate_password_hash(password).decode('utf-8'))

    try:
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Registration failed. {str(e)}', 'danger')

    # Save to Excel
    excel_file_path = os.path.join(app.instance_path, 'register.xlsx')
    data = {'Username': [username], 'Email': [email], 'Password': [password]}
    save_to_excel(data, excel_file_path)

    return render_template('register.html', registered=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
