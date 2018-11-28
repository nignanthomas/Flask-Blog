from flask import Blueprint

users = Blueprint('users',__name__)


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



################################################################################


@app.route('/account', methods =['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'photos/'+current_user.image_file)
    return render_template('account.html', form = form, title = 'Flask Blog -- My Account', image_file = image_file)


################################################################################
@app.route("/user/<string:username>")
def user_posts(username):
    # posts = Post.query.all()
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1,type=int)
    #use backslash '\' to break python lines
    posts = Post.query.filter_by(author=user)\
                        .order_by(Post.date_posted.desc())\
                        .paginate(page=page, per_page=5)

    return render_template('user_posts.html', posts = posts, user = user, title = 'Flask Blog -- '+user.username)

################################################################################


@app.route('/reset_password', methods =['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form = form, title = 'Flask Blog -- Reset Password')



@app.route('/reset_password/<token>', methods =['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or Expired Token!', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.username.data).decode('utf-8')
        user.password =  hashed_password
        db.session.commit()
        flash(f'Your paasword has been updated! Feel free to login now.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_token.html', form = form, title = 'Flask Blog -- Reset Password')
