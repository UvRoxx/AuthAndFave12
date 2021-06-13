from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'gb-auth-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask Login

login_manager = LoginManager()
login_manager.init_app(app)


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000), primary_key=True)


db.create_all()


@app.route('/')
def home():
    return "Welcome To User Manager A.P.I - D.T.I"


@app.route('/add/<uid>/<ups>', methods=['GET', 'POST'])
def register(uid, ups):
    name = uid
    password = ups
    password = generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=2)
    print(password)
    new_user = User(name=name, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "user_name": name,
            "password": password,
            "progress": "success",

        })
    except:
        return jsonify({"Error": "Unknown Server Error Occurred"})


@app.route('/login/<uid>/<ups>', methods=['GET', 'POST'])
def login(uid, ups):
    try:
        user = User.query.filter_by(name=uid).first()
        if check_password_hash(user.password, ups):
            return jsonify({"status": 'success'})
        else:
            return jsonify({"status": 'invalid_pass'})
    except AttributeError:
        return jsonify({"status": 'no_user_found'})





if __name__ == "__main__":
    app.run(debug=True)
