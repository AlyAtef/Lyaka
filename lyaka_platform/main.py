# lyaka_platform/main.py
import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from lyaka_platform import db
from lyaka_platform.models import User
from lyaka_platform.forms import UpdateProfileForm

main = Blueprint("main", __name__)

# --- دالة حفظ الصورة ---
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    # إنشاء مجلد profile_pics إذا لم يكن موجوداً
    output_dir = os.path.join(current_app.root_path, 'static/profile_pics')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # تغيير حجم الصورة
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# --- المسارات ---
@main.route("/")
@main.route("/news_feed")
def news_feed():
    return render_template("news_feed.html", title="الأخبار")

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", title="لوحة التحكم")

@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('تم تحديث ملفك الشخصي بنجاح!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("profile.html", title="ملفي الشخصي", image_file=image_file, form=form)

# ... (باقي المسارات كما هي بدون تغيير) ...
@main.route("/events")
@login_required
def events():
    return render_template("events.html", title="الأحداث")

@main.route("/active_workout")
@login_required
def active_workout():
    return render_template("active_workout.html", title="بدء التمرين")

@main.route("/health_tip")
@login_required
def health_tip():
    return render_template("health_tip.html", title="نصيحة اليوم الصحية")

@main.route("/exercises")
@login_required
def exercises():
    mock_exercises = [
        {'name': 'تمرين الضغط (Bench Press)', 'body_part': 'الصدر', 'image': 'images/bench_press.jpg'},
        {'name': 'تمرين القرفصاء (Squat)', 'body_part': 'الأرجل', 'image': 'images/squat.jpg'},
    ]
    return render_template("exercises.html", title="التمارين", exercises=mock_exercises)

@main.route("/live_tv")
@login_required
def live_tv():
    return render_template("live_tv.html", title="البث المباشر")

@main.route("/clubs")
@login_required
def clubs():
    return render_template("clubs.html", title="الأندية والجيمات")

@main.route("/stopwatch")
@login_required
def stopwatch():
    return render_template("stopwatch.html", title="ساعة التوقيت")
