# lyaka_platform/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from lyaka_platform.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    password = PasswordField('كلمة المرور', validators=[DataRequired()])
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('إنشاء حساب')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('اسم المستخدم هذا محجوز. الرجاء اختيار اسم آخر.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('هذا البريد الإلكتروني محجوز. الرجاء اختيار بريد آخر.')

class LoginForm(FlaskForm):
    credential = StringField('اسم المستخدم أو البريد الإلكتروني', validators=[DataRequired()])
    password = PasswordField('كلمة المرور', validators=[DataRequired()])
    remember = BooleanField('تذكرني')
    submit = SubmitField('تسجيل الدخول')

class UpdateProfileForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    picture = FileField('تحديث صورة الملف الشخصي', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    
    gender = SelectField('الجنس', choices=[('Male', 'ذكر'), ('Female', 'أنثى')])
    age = IntegerField('العمر')
    weight_kg = FloatField('الوزن (كجم)')
    height_cm = FloatField('الطول (سم)')
    fitness_goal = StringField('الهدف الرياضي')
    activity_level = SelectField('مستوى النشاط', choices=[
        ('sedentary', 'خامل (عمل مكتبي)'),
        ('light', 'نشاط خفيف (تمارين 1-3 أيام/أسبوع)'),
        ('moderate', 'نشاط معتدل (تمارين 3-5 أيام/أسبوع)'),
        ('active', 'نشيط (تمارين 6-7 أيام/أسبوع)'),
        ('very_active', 'نشيط جداً (تمارين شاقة يومياً)')
    ])
    
    submit = SubmitField('تحديث')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('اسم المستخدم هذا محجوز. الرجاء اختيار اسم آخر.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            # هذا هو السطر الذي تم تصحيحه (تمت إزالة المسافة الزائدة)
            if user:
                raise ValidationError('هذا البريد الإلكتروني محجوز. الرجاء اختيار بريد آخر.')

# --- Other Forms (can be completed later) ---

class ExerciseForm(FlaskForm):
    name = StringField('اسم التمرين', validators=[DataRequired()])
    body_part = StringField('الجزء المستهدف من الجسم', validators=[DataRequired()])
    description = TextAreaField('الوصف')
    submit = SubmitField('إضافة تمرين')

class WorkoutPlanForm(FlaskForm):
    name = StringField('اسم خطة التمرين', validators=[DataRequired()])
    description = TextAreaField('الوصف')
    submit = SubmitField('إنشاء خطة')

class ChannelForm(FlaskForm):
    name = StringField('اسم القناة', validators=[DataRequired()])
    description = TextAreaField('وصف القناة')
    submit = SubmitField('إنشاء قناة')

class ChannelVideoForm(FlaskForm):
    title = StringField('عنوان الفيديو', validators=[DataRequired()])
    video_url = StringField('رابط الفيديو (YouTube, etc.)', validators=[DataRequired()])
    submit = SubmitField('إضافة فيديو')
