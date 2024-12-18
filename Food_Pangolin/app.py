from flask import Flask, render_template, request, url_for, session, redirect
from functools import wraps
from modules import init

app = Flask(__name__, static_folder = 'static', static_url_path = '/')
app.config['SECRET_KEY'] = '123TyU%^&'

def login_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		loginID = session.get('loginID')
		if not loginID:
			return redirect('/login.html')
		return f(*args, **kwargs)
	return wrapper


@app.route("/", methods=['GET','POST']) 
@login_required
def homepage():
	return redirect("register.html")

@app.route("/register", methods=['GET','POST'])
def register():
	if request.method == "GET":
		return redirect("/register.html")
	
	form = request.form
	name = form['NAME']
	mail = form['MAIL']
	pwd = form['PWD']
	role = form['role']
	user_from_mail = init.check_account(mail, pwd)
	if user_from_mail == []:
		init.regsiter(name, mail, pwd, role)
	return redirect("/register.html")

@app.route("/login", methods=['GET','POST'])
def login():
	if request.method == "GET":
		return redirect("/login.html")
	form = request.form
	mail = form['MAIL']
	pwd = form['PWD']
	user_from_mail = init.check_account(mail, pwd)
	if user_from_mail == []:
		return redirect("/login.html")
	return redirect("/register.html")