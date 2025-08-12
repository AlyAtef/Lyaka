# lyaka_platform/auth.py

from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from lyaka_platform import db, bcrypt
from lyaka_platform.models import User
from lyaka_platform.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # إذا كان المستخدم مسجلاً دخوله بالفعل، وجهه إلى صفحة الأخبار
        return redirect(url_for('main.news_feed'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('تم إنشاء حسابك بنجاح! يمكنك الآن تسجيل الدخول.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='إنشاء حساب', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # إذا كان المستخدم مسجلاً دخوله بالفعل، وجهه إلى صفحة الأخبار
        return redirect(url_for('main.news_feed'))
        
    form = LoginForm()
    if form.validate_on_submit():
        # --- Debugging Prints ---
        print("--- Login attempt ---")
        print(f"Form submitted: {form.is_submitted()}")
        print(f"Form validates on submit: {form.validate_on_submit()}")
        print(f"Form errors: {form.errors}")
        
        credential = form.credential.data
        password = form.password.data
        
        print(f"Credential from form: '{credential}'")
        print(f"Password from form: '{password}'")

        user = User.query.filter((User.username == credential) | (User.email == credential)).first()

        if user:
            print("--- User found in database ---")
            print(f"User ID: {user.id}, Username: {user.username}, Email: {user.email}")
            print(f"Hashed password from DB: '{user.password}'")
            
            password_check = bcrypt.check_password_hash(user.password, password)
            print(f"Password check result: {password_check}")

            if password_check:
                print("--- Password is correct. Logging in user. ---")
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                # وجه المستخدم إلى صفحة الأخبار بعد تسجيل الدخول
                return redirect(next_page) if next_page else redirect(url_for('main.news_feed'))
            else:
                print("--- Incorrect password. ---")
                flash('فشل تسجيل الدخول. يرجى التحقق من البريد الإلكتروني/اسم المستخدم وكلمة المرور', 'danger')
        else:
            print("--- User not found. ---")
            flash('فشل تسجيل الدخول. يرجى التحقق من البريد الإلكتروني/اسم المستخدم وكلمة المرور', 'danger')
            
    return render_template('auth/login.html', title='تسجيل الدخول', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    # وجه المستخدم إلى صفحة الأخبار بعد تسجيل الخروج
    return redirect(url_for('main.news_feed'))
