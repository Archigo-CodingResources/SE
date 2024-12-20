from flask import Flask, render_template, request, session, redirect
from functools import wraps
from modules import init, restaurant

app = Flask(__name__, static_folder="static", static_url_path="/")
app.config['SECRET_KEY'] = '123TyU%^&'


# 登錄驗證
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
    dest = '/restaurant/menu.html' if session['role'] == 0 else "delivery/order_list.html" if session['role'] == 1 else 'client/restaurant.html'
    data = [{}]
    if session['role'] == 2:
        data = [{
            "name":session['name'],
            "data":restaurant.get_restaurant()
            }]
    return render_template(dest, data=data)

@app.route("/menu", methods=['GET']) 
@login_required
def menu():
    form = request.args
    rid = form['id']
    data = [{
        "name":session['name'],
        "data":restaurant.get_menu(int(rid))
        }]
    return render_template("client/menu.html", data=data)

@app.route("/cart", methods=['POST']) 
@login_required
def cart():
    form = request.form
    return render_template("client/menu.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return redirect("register.html")
    
    # 处理 POST 请求（提交注册表单）
    form = request.form
    name = form['NAME']
    mail = form['MAIL']
    pwd = form['PWD']
    role = form['ROLE']
    
    # 检查用户是否已存在
    user_from_mail = init.check_account(mail, pwd)
    if user_from_mail == []:
        # 如果没有找到，进行注册
        init.register(name, mail, pwd, role)
        return redirect("/login.html")  # 注册后跳转到登录页面
    
    return redirect("/register.html")  # 如果注册失败，重新返回注册页面

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return redirect("/login.html")
    
    # 处理 POST 请求（提交登录表单）
    form = request.form
    mail = form['MAIL']
    pwd = form['PWD']
    
    # 检查用户凭据
    user_from_mail = init.check_account(mail, pwd)

    if user_from_mail == []:
        return redirect("/login")
    
    # 登录成功，保存用户登录信息到 session
    session['loginID'] = mail
    session['name'] = user_from_mail[0]['name']
    session['role'] = user_from_mail[0]['role']
    return redirect("/")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")
