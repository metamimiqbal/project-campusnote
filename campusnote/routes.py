from flask import Flask, render_template, url_for, request, redirect, flash
from campusnote.models import RegisterForm, LoginForm
from campusnote import app, db




@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f'Account created successfully for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #checker -> database
        return redirect(url_for('home'))
        
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    pass   

@app.route('/account')
def account():
    pass   

@app.route('/browse')
def browse():
    pass   

@app.route('/search')
def search():
    pass   

@app.route('/upload')
def upload():
    pass   

