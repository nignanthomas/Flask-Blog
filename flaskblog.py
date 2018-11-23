from flask import Flask,render_template,url_for,flash,redirect
from forms import RegistrationForm,LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '12345qwerty6789'





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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data} !!!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form = form, title = 'Flask Blog -- Register')


@app.route('/login', methods =['GET','POST'])
def register():)
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', form = form, title = 'Flask Blog -- Login')







if __name__ == '__main__':
    app.run(debug=True)
