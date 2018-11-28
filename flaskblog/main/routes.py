from flask import Blueprint

main = Blueprint('main',__name__)




@main.route("/")
@main.route("/home")
def home():
    # posts = Post.query.all()
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('home.html', posts = posts, title = 'Flask Blog -- Home')


@main.route("/about")
def about():
    return render_template('about.html', title = 'Flask Blog -- About')