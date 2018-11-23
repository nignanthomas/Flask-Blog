from flask import Flask,render_template,url_for
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



if __name__ == '__main__':
    app.run(debug=True)
