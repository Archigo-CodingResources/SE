from flask import Flask, render_template, request, url_for, session, redirect

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
	pass