import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, request, redirect, flash
from campusnote.forms import RegisterForm, LoginForm, UpdateAccountForm, UploadNoteForm
from campusnote import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from campusnote.models import User, Note, Rating, University, Department, Year, Semester, Subject
ALLOWED_NOTE_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}
from sqlalchemy import or_


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email = form.email.data, password = pw_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully for {form.username.data}', 'success')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/browse')
def browse():
    uni_id = request.args.get('uni', type=int)
    dept_id = request.args.get('dept', type=int)
    year_id = request.args.get('year', type=int)
    sem_id = request.args.get('sem', type=int)
    sub_id = request.args.get('sub', type=int)

    context = {
        'universities': None,
        'departments': None,
        'years': None,
        'semesters': None,
        'subjects': None,
        'notes': None,
        'selected_uni': uni_id,
        'selected_dept': dept_id,
        'selected_year': year_id,
        'selected_sem': sem_id,
        'selected_sub': sub_id
    }

    if not uni_id:
        context['universities'] = University.query.order_by(University.name).all()
    elif not dept_id:
        context['departments'] = Department.query.filter_by(university_id=uni_id).order_by(Department.name).all()
    elif not year_id:
        context['years'] = Year.query.filter_by(department_id=dept_id).order_by(Year.label).all()
    elif not sem_id:
        context['semesters'] = Semester.query.filter_by(year_id=year_id).order_by(Semester.label).all()
    elif not sub_id:
        context['subjects'] = Subject.query.filter_by(semester_id=sem_id).order_by(Subject.name).all()
    else:
        context['notes'] = Note.query.filter_by(subject_id=sub_id).order_by(Note.uploaded_at.desc()).all()

    return render_template('browse.html', **context)


# upload notes.
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadNoteForm()

    form.university_id.choices = [(u.id, u.name) for u in University.query.order_by(University.name).all()]
    form.department_id.choices = [(d.id, f"{d.name} ({d.university.name})") for d in Department.query.join(University).order_by(Department.name).all()]
    form.year_id.choices = [(y.id, f"{y.label} ({y.department.name})") for y in Year.query.join(Department).order_by(Year.label).all()]
    form.semester_id.choices = [(s.id, f"{s.label} ({s.year.label})") for s in Semester.query.join(Year).order_by(Semester.label).all()]
    form.subject_id.choices = [(s.id, f"{s.name} ({s.semester.label})") for s in Subject.query.join(Semester).order_by(Subject.name).all()]

    if form.validate_on_submit():
        department = Department.query.filter_by(
            id=form.department_id.data,
            university_id=form.university_id.data
        ).first()

        year = Year.query.filter_by(
            id=form.year_id.data,
            department_id=form.department_id.data
        ).first()

        semester = Semester.query.filter_by(
            id=form.semester_id.data,
            year_id=form.year_id.data
        ).first()

        subject = Subject.query.filter_by(
            id=form.subject_id.data,
            semester_id=form.semester_id.data
        ).first()

        if not all([department, year, semester, subject]):
            flash('Invalid hierarchy selection. Please choose matching University > Department > Year > Semester > Subject.', 'danger')
            return render_template('upload_notes.html', form=form)

        relative_path = save_note_file(form.note_file.data)
        if not relative_path:
            flash('Invalid file type. Allowed: PDF, JPG, JPEG, PNG.', 'danger')
            return render_template('upload_notes.html', form=form)

        note = Note(
            title=form.title.data.strip(),
            description=(form.description.data or '').strip() or None,
            file_path=relative_path,
            user_id=current_user.id,
            subject_id=subject.id
        )
        db.session.add(note)
        db.session.commit()

        flash('Note uploaded successfully.', 'success')
        return redirect(url_for('upload'))

    return render_template('upload_notes.html', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_pic = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    return render_template('account.html', title='Account', profile_pic=profile_pic, form=form)


def save_note_file(file_storage):
    _, ext = os.path.splitext(file_storage.filename or '')
    ext = ext.lower()
    if ext not in ALLOWED_NOTE_EXTENSIONS:
        return None

    upload_dir = os.path.join(app.root_path, 'static', 'uploads', 'notes')
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{secrets.token_hex(16)}{ext}"
    absolute_path = os.path.join(upload_dir, filename)
    file_storage.save(absolute_path)

    return os.path.join('uploads', 'notes', filename).replace('\\', '/')


@app.route('/search')
def search():
    q = (request.args.get('q') or '').strip()
    uni_id = request.args.get('uni', type=int)
    dept_id = request.args.get('dept', type=int)
    year_id = request.args.get('year', type=int)
    sem_id = request.args.get('sem', type=int)
    sub_id = request.args.get('sub', type=int)

    query = (Note.query
             .join(Subject, Note.subject_id == Subject.id)
             .join(Semester, Subject.semester_id == Semester.id)
             .join(Year, Semester.year_id == Year.id)
             .join(Department, Year.department_id == Department.id)
             .join(University, Department.university_id == University.id))

    if q:
        query = query.filter(or_(
            Note.title.ilike(f"%{q}%"),
            Note.description.ilike(f"%{q}%"),
            Subject.name.ilike(f"%{q}%")
        ))

    if uni_id:
        query = query.filter(University.id == uni_id)
    if dept_id:
        query = query.filter(Department.id == dept_id)
    if year_id:
        query = query.filter(Year.id == year_id)
    if sem_id:
        query = query.filter(Semester.id == sem_id)
    if sub_id:
        query = query.filter(Subject.id == sub_id)

    results = query.order_by(Note.uploaded_at.desc()).all()

    return render_template(
        'search.html',
        results=results,
        q=q,
        universities=University.query.order_by(University.name).all(),
        departments=Department.query.order_by(Department.name).all(),
        years=Year.query.order_by(Year.label).all(),
        semesters=Semester.query.order_by(Semester.label).all(),
        subjects=Subject.query.order_by(Subject.name).all(),
        selected_uni=uni_id,
        selected_dept=dept_id,
        selected_year=year_id,
        selected_sem=sem_id,
        selected_sub=sub_id
    )