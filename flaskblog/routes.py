from flask import render_template,url_for,flash,redirect,request
from flaskblog import app,db,bcrypt
from flaskblog.forms import RegistrationForm,LoginForm
from flaskblog.models import User, Post
from flask_login import login_user,current_user,logout_user,login_required






posts = [
    {
        'author': 'Nie Senfan',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': 'November 22, 2018'
    },
    {
        'author': 'Nyakio Mburu',
        'title': 'Blog Post 2',
        'content': 'Seconf pst content',
        'date_posted': 'November 25, 2018'
    }

]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts)


@app.route("/about")
def about():
    return render_template('about.html', title = 'About')



@app.route('/register', methods =['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.username.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! Feel free to login now.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form = form, title = 'Flask Blog -- Register')


@app.route('/login', methods =['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash(f'Successfully Logged In. Welcome {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', form = form, title = 'Flask Blog -- Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/account')
@login_required
def account():

    return render_template('account.html', title = 'Flask Blog -- My Account')
