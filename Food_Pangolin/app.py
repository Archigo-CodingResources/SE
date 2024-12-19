from flask import Flask, render_template, request, session, redirect
from functools import wraps
# from flask_sqlalchemy import SQLAlchemy
from modules import init

app = Flask(__name__, static_folder="static", static_url_path="/")
app.config['SECRET_KEY'] = '123TyU%^&'

# # 數據庫鏈接
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'  # 記得幫我更換數據庫的URL
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # 模型
# class Menu(db.Model):
#     __tablename__ = 'menu'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float, nullable=False)

# # 獲取菜單數據
# def get_vendor_menu():
#     menu_items = Menu.query.all()
#     return [{'name': item.name, 'price': item.price} for item in menu_items]

# 登錄驗證
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        loginID = session.get('loginID')
        if not loginID:
            return redirect('/login.html')  # 如果沒有登錄跳轉到登錄界面
        return f(*args, **kwargs)
    return wrapper

@app.route("/", methods=['GET', 'POST']) 
@login_required
def homepage():
    # 獲取數據中菜單數據
    menu = [{}]
    myname = session.get('loginID', 'User')  # 獲取用戶登錄名稱
    return render_template('/client/menu.html', menu=menu, myname=myname)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return redirect("register.html")
    
    form = request.form
    name = form['NAME']
    mail = form['MAIL']
    pwd = form['PWD']
    role = form['ROLE']
    
    # 查看用戶是否存在
    user_from_mail = init.check_account(mail, pwd)
    if user_from_mail == []:
        init.register(name, mail, pwd, role)
        return redirect("/login.html")
    
    return redirect("/register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return redirect("/login.html")
    
    form = request.form
    mail = form['MAIL']
    pwd = form['PWD']
    
    # 檢查用戶憑證
    user_from_mail = init.check_account(mail, pwd)
    print(user_from_mail)
    if user_from_mail == []:
        return redirect("/login")
    
    # 登錄成功並保存用戶信息 session
    session['loginID'] = mail
    return redirect("/")
