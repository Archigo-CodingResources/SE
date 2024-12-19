from flask import Flask, render_template, request, url_for, session, redirect
from functools import wraps
from modules import init

app = Flask(__name__, static_folder='static', static_url_path='/')
app.config['SECRET_KEY'] = '123TyU%^&'

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
    # 登录后重定向到注册页面（你可以根据需要更改）
    return redirect("register.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        # 如果是 GET 请求，直接返回注册页面
        return render_template("register.html")
    
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
        # 如果是 GET 请求，返回登录页面
        return render_template("login.html")
    
    # 处理 POST 请求（提交登录表单）
    form = request.form
    mail = form['MAIL']
    pwd = form['PWD']
    
    # 检查用户凭据
    user_from_mail = init.check_account(mail, pwd)
    if user_from_mail == []:
        # 用户不存在或密码错误，跳转回登录页面
        return redirect("/login.html")
    
    # 登录成功，保存用户登录信息到 session
    session['loginID'] = mail
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
