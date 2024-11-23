'''
from flask import render_template, url_for, flash, redirect
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)




from app import app, db
from flask import render_template, request, redirect, url_for, session
import psycopg2
from functools import wraps

# Decorator để kiểm tra đăng nhập
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('connect'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('index.html', version=session.get('db_version'))

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    if request.method == 'POST':
        database_name = request.form['database_name']
        username = request.form['username']
        password = request.form['password']
        host = request.form['host']
        port = request.form['port']

        try:
            # Thử kết nối database
            conn = psycopg2.connect(
                database=database_name,
                user=username,
                password=password,
                host=host,
                port=port
            )
            
            # Lấy version của database
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            
            # Lưu thông tin vào session
            session['logged_in'] = True
            session['db_version'] = version
            session['db_credentials'] = {
                'database': database_name,
                'user': username,
                'password': password,
                'host': host,
                'port': port
            }
            
            cur.close()
            conn.close()
            
            return redirect(url_for('index'))
            
        except (Exception, psycopg2.Error) as error:
            return render_template('connect.html', error=str(error))

    return render_template('connect.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('connect'))
'''

import bcrypt
from app import app, db
from flask import flash, render_template, request, redirect, url_for, session
import psycopg2
from functools import wraps
from psycopg2 import sql

from app.forms import RegistrationForm
from app.models import User

from app.forms import LoginForm

'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Xử lý đăng nhập (kiểm tra email và mật khẩu ở đây)
        if email == "user@example.com" and password == "password123":  # Kiểm tra đơn giản
            return redirect(url_for('home'))  # Chuyển hướng về trang chủ sau khi đăng nhập thành công
        else:
            return "Sai thông tin đăng nhập", 401  # Xử lý khi đăng nhập sai
    return render_template('login.html')
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                session['logged_in'] = True
                session['user_id'] = user.id
                session['email'] = user.email
                
                flash('Đăng nhập thành công!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Email hoặc mật khẩu không đúng. Vui lòng thử lại.', 'danger')
                
        except Exception as e:
            flash('Có lỗi xảy ra khi đăng nhập. Vui lòng thử lại.', 'danger')
            print(f"Login error: {str(e)}")  # Log lỗi để debug
            
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Tài khoản của bạn đã được tạo thành công!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)
@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    if request.method == 'POST':
        database_name = request.form['database_name']
        username = request.form['username']
        password = request.form['password']
        host = request.form['host']
        port = request.form['port']

        try:
            conn = psycopg2.connect(
                database=database_name,
                user=username,
                password=password,
                host=host,
                port=port
            )
            
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            
            session['logged_in'] = True
            session['db_version'] = version
            session['db_credentials'] = {
                'database': database_name,
                'user': username,
                'password': password,
                'host': host,
                'port': port
            }
            
            cur.close()
            conn.close()
            
            return redirect(url_for('check_connection'))
            
        except (Exception, psycopg2.Error) as error:
            return render_template('connect.html', error=str(error))

    return render_template('connect.html')

@app.route('/check_connection')
def check_connection():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html', db_version=session['db_version'])
    return redirect(url_for('connect'))

@app.route('/home')

def home():
    if 'logged_in' in session and session['logged_in']:
        return render_template('home.html', username=session['db_credentials']['user'])
    return redirect(url_for('connect'))


#Connect---
db_config = {
    'dbname': 'baitap2',
    'user': 'postgres',
    'password': '171104',
    'host': 'localhost',
    'port': '5432'
}

def connect():
    """Kết nối với cơ sở dữ liệu PostgreSQL."""
    return psycopg2.connect(**db_config)


@app.route('/quan-ly-database')
def database():
    """Trang chủ, hiển thị dữ liệu từ bảng."""
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM danhsachtruyen")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('database.html', rows=rows)
    except Exception as e:
        flash(f"Error loading data: {e}", 'error')
        return render_template('database.html', rows=[])


@app.route('/insert', methods=['POST'])
def insert_data():
    """Chèn dữ liệu vào cơ sở dữ liệu."""
    try:
        tentruyen = request.form['tentruyen']
        taptruyen = request.form['taptruyen']
        sotrang = request.form['sotrang']
        theloai = request.form['theloai']
        
        conn = connect()
        cur = conn.cursor()
        query = sql.SQL("INSERT INTO danhsachtruyen (tentruyen, taptruyen, sotrang, theloai) VALUES (%s, %s, %s, %s)")
        cur.execute(query, (tentruyen, taptruyen, sotrang, theloai))
        conn.commit()
        cur.close()
        conn.close()
        
        flash('Data inserted successfully!', 'success')
        return redirect(url_for('database'))
    except Exception as e:
        flash(f"Error inserting data: {e}", 'error')
        return redirect(url_for('database'))


@app.route('/search', methods=['POST'])
def search_data():
    """Tìm kiếm dữ liệu trong bảng."""
    search_keyword = request.form['search_keyword']
    try:
        conn = connect()
        cur = conn.cursor()
        query = sql.SQL("SELECT * FROM danhsachtruyen WHERE tentruyen ILIKE %s OR taptruyen ILIKE %s")
        cur.execute(query, (f"%{search_keyword}%", f"%{search_keyword}%"))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('database.html', rows=rows)
    except Exception as e:
        flash(f"Error searching data: {e}", 'error')
        return redirect(url_for('database'))



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('connect'))
