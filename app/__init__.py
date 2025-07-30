from flask import (
    Flask,
    Blueprint,
    render_template,
    url_for,
    request,
    redirect,
    session,
    flash,
    g,
)
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

from .db import Base, User, Device
from .forms import RegisterForm, LoginForm

dtb = SQLAlchemy(model_class=Base)
bp = Blueprint("root", __name__, template_folder="templates/")


def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if not hasattr(g, "user") or g.user is None:
            return redirect(url_for("root.login"))
        return f(*args, **kwargs)

    return decorated_func


def logout_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if hasattr(g, "user") and g.user is not None:
            return redirect(url_for("root.index"))
        return f(*args, **kwargs)

    return decorated_func


def load_user():
    id = session.get("user_id")
    if id:
        g.user = dtb.session.query(User).filter_by(id=id).first()
    else:
        g.user = None


def create_app():
    app = Flask(__name__)
    # Set config. Should be somewhere else. too tired
    app.config.update(
        {
            "SECRET_KEY": "Very-Secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///database.db",
        }
    )
    dtb.init_app(app)
    with app.app_context():
        dtb.create_all()

    app.before_request(load_user)

    app.register_blueprint(bp)

    return app


@bp.route("/")
@login_required
def index():
    return render_template("index.html")


@bp.route("/register/", methods=["GET", "POST"])
@logout_required
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if dtb.session.query(User).filter_by(email=form.email.data).first():
            flash("Account exists. Please login instead")
            return render_template(
                "auth.html",
                form=RegisterForm(),
                form_action=url_for("root.register"),
                sec_btn_href=url_for("root.login"),
                sec_btn_txt="Login",
            )
        user = User(form.email.data, form.password.data, form.birthdate.data)
        ua = request.headers.get("User-Agent")

        if not dtb.session.query(Device).filter_by(user_agent=ua).first():
            _ = Device(user, ua)
        dtb.session.add(user)  # device will be added along with user
        dtb.session.commit()

        flash("Account creation success")
        return redirect(url_for("root.login"))
    else:
        return render_template(
            "auth.html",
            form=RegisterForm(),
            form_action=url_for("root.register"),
            sec_btn_href=url_for("root.login"),
            sec_btn_txt="Login",
        )


@bp.route("/login/", methods=["GET", "POST"])
@logout_required
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = dtb.session.query(User).filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            session["user_id"] = user.id
            return redirect(url_for("root.index"))
        else:
            flash("Wrong email or password")
    return render_template(
        "auth.html",
        form=LoginForm(),
        form_action=url_for("root.login"),
        sec_btn_href=url_for("root.register"),
        sec_btn_txt="Register",
    )


@bp.route("/logout/")
@login_required
def logout():
    session.clear()
    g.user = None
    return redirect(url_for("root.login"))
