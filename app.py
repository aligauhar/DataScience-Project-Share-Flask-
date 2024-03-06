from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pandas as pd
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  

class Contact(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=False)
    query = db.Column(db.Text, nullable=False)

class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Discription = db.Column(db.String(120), nullable=False)
    Category = db.Column(db.String(50), nullable=True)
    Go_to_File = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'Name': self.Name,
            'Discription': self.Discription,
            'Category': self.Category,
            'Go_to_File': self.Go_to_File,
        }

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Discription = db.Column(db.String(120), nullable=False)
    Category = db.Column(db.String(50), nullable=True)
    Go_to_File = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'Name': self.Name,
            'Discription': self.Discription,
            'Category': self.Category,
            'Go_to_File': self.Go_to_File,
        }

# ------------------------saving data to the CSV-------------------------
    
def save_Contect_to_db(data, db_file_path):
    if os.path.exists(db_file_path):
        df = pd.read_excel(db_file_path)
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    else:
        df = pd.DataFrame(data)

    df.to_excel(db_file_path, index=False)

def Register_to_db(data, db_file_path):
    if os.path.exists(db_file_path):
        df = pd.read_excel(db_file_path)
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    else:
        df = pd.DataFrame(data)

    df.to_excel(db_file_path, index=False)

# -------------------------other cotributions

def save_Project_to_db(data, db_file_path):
    if os.path.exists(db_file_path):
        df = pd.read_excel(db_file_path)
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    else:
        df = pd.DataFrame(data)

    df.to_excel(db_file_path, index=False)

# -------------------------other cotributions
    
def save_Model_to_db(data, db_file_path):
    if os.path.exists(db_file_path):
        df = pd.read_excel(db_file_path)
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    else:
        df = pd.DataFrame(data)

    df.to_excel(db_file_path, index=False)

# ---------------------------reading data from CSV-----------------------

def read_model_file():
    data = Model.query.all()
    if data:
        return [item.to_dict() for item in data]
    else:
        return []

def read_project_file():
    data = Project.query.all()
    if data:
        return [item.to_dict() for item in data]
    else:
        return []

#  ----------------------- for login
def read_registeration_file(db_file_path):
    if os.path.exists(db_file_path):
        df = pd.read_excel(db_file_path)
        return df.to_dict(orient='records')
    else:
        return []


# -----------------------------------routes-------------------------------
                  
@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/mainpage.html')
def mainpage():
    return render_template('mainpage.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('mainpage.html')

# -------------------------------Process Form------------------------
@app.route('/login_form', methods=['POST'])
def login_form():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Register.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            # Passwords match, set the email in the session
            session.permanent = True
            session['email'] = email
            products = read_project_file()
            return render_template('project.html', products=products, message = "success")
       
        # If login fails, you may want to display an error message
        error_message = "Invalid email or password"
        return render_template('login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/mainpage.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    name = request.form.get('name')
    email = request.form.get('email')
    query = request.form.get('query')

    contact_info = Contact(name=name, email=email, query=query)
    db.session.add(contact_info)
    db.session.commit()

    # Save to Excel
    db_file_path = os.path.join(app.instance_path, 'contact.xlsx')
    data = {'Name': [name], 'Email': [email], 'Query': [query]}
    save_Contect_to_db(data, db_file_path)

    return render_template('contact.html', sent=True)

@app.route('/model.html')
def model():
    products = read_model_file()
    return render_template('model.html', products=products)

@app.route('/project.html')
def project(): 
    products = read_project_file()
    return render_template('project.html', products=products)


@app.route('/process_register', methods=['POST'])
def process_register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    encryptedpass = bcrypt.generate_password_hash(password).decode('utf-8')

    # Check if the email is already registered
    existing_user = Register.query.filter_by(email=email).first()

    if existing_user:
        flash('Email already registered. Please use a different email.', 'danger')
        return render_template('register.html', exist=True)

    # If email is not present, proceed with registration
    user = Register(username=username, email=email, password_hash=encryptedpass)

    try:
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Registration failed. {str(e)}', 'danger')

    # Save to Excel
    db_file_path = os.path.join(app.instance_path, 'register.xlsx')
    data = {'Username': [username], 'Email': [email], 'Password': [encryptedpass]}
    Register_to_db(data, db_file_path)

    return render_template('register.html', registered=True)

# ---------------------model and project adddition form-----------------

@app.route('/add_model')
def add_model():
    return render_template('add_model_form.html')

@app.route('/submit_model', methods=['POST'])
def submit_model():

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        go_to_file = request.form['go_to_file']

        # Assuming you have a Model model, adjust this based on your actual model structure
        new_model = Project(Name=name, Discription=description, Category=category, Go_to_File=go_to_file)
        db.session.add(new_model)
        db.session.commit()
        products = read_project_file()
        return render_template('project.html', products=products, saved=True)

    return redirect('/add_model')  # Redirect to the form page if a GET request is received


# ------------------------------main function--------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

