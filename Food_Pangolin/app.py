from flask import Flask, render_template, request, session, redirect
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from modules import init

app = Flask(__name__)
app.config['SECRET_KEY'] = '123TyU%^&'

# 配置数据库连接（假设使用 SQLite）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'  # 你可以根据需要更换成其他数据库的连接URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义数据库模型
class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

# 获取菜单数据
def get_vendor_menu():
    menu_items = Menu.query.all()
    return [{'name': item.name, 'price': item.price} for item in menu_items]

# 登录验证装饰器
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        loginID = session.get('loginID')
        if not loginID:
            return redirect('/login.html')  # 如果没有登录，跳转到登录页面
        return f(*args, **kwargs)
    return wrapper

@app.route("/", methods=['GET', 'POST']) 
@login_required
def homepage():
    # 登录后重定向到菜单页面
    return redirect("/menu")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    form = request.form
    name = form['NAME']
    mail = form['MAIL']
    pwd = form['PWD']
    role = form['ROLE']
    
    # 检查用户是否已存在
    user_from_mail = init.check_account(mail, pwd)
    if user_from_mail == []:
        init.register(name, mail, pwd, role)
        return redirect("/login.html")
    
    return redirect("/register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    form = request.form
    mail = form['MAIL']
    pwd = form['PWD']
    
    # 检查用户凭据
    user_from_mail = init.check_account(mail, pwd)
    if user_from_mail == []:
        return redirect("/login.html")
    
    # 登录成功，保存用户登录信息到 session
    session['loginID'] = mail
    return redirect("/")

@app.route('/menu')
@login_required
def menu():
    # 获取数据库中的菜单数据
    menu = get_vendor_menu()
    myname = session.get('loginID', 'User')  # 获取用户的登录名（假设使用session保存用户的邮件作为登录ID）
    return render_template('menu.html', menu=menu, myname=myname)

if __name__ == '__main__':
    app.run(debug=True)
