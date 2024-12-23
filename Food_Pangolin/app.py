from flask import Flask, render_template, request, session, redirect
from functools import wraps
from datetime import datetime
from modules import init, client, restaurant, delivery
from importlib import reload

app = Flask(__name__, static_folder="static", static_url_path="/")
app.config['SECRET_KEY'] = '123TyU%^&'

def reload_db():
    reload(init)
    reload(restaurant)
    reload(client)
    reload(delivery)


# 登錄驗證
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        loginID = session.get('loginID')
        if not loginID:
            return redirect('/login.html')  # 如果沒登錄跳轉至登錄界面
        return f(*args, **kwargs)
    return wrapper

@app.route("/", methods=['GET', 'POST']) 
@login_required
def homepage():
    reload_db()
    #0(用戶)，1(外送員),2(商家)
    dest = '/restaurant/order.html' if session['role'] == 0 else "delivery/order_list.html" if session['role'] == 1 else 'client/restaurant.html'

    if session['role'] == 0:
        cart = restaurant.get_order(int(session['id']))
        cart_data = restaurant.compose_order(cart)

        data = [
            {
                "name":session['name'],
                "data":cart_data
                }
            ]
        
    elif session['role'] == 1:
        order = delivery.get_order()
        order_data = delivery.compose_order(order)

        data = [{
            "name":session['name'],
            "data":order_data
            }]

    elif session['role'] == 2:
        data = [{
            "name":session['name'],
            "data":client.get_restaurant()
            }]
        
    return render_template(dest, data=data)



@app.route("/addfoodUI", methods=['GET']) 
@login_required
def addfood():
    reload_db()
    form = request.args
    rid = form['id']
    dest = '/restaurant/addfoodUI.html'
    return render_template(dest, rid = rid)


@app.route("/addfood", methods=['GET', 'POST']) 
@login_required
def add():
    reload_db()
    form = request.form
    rid = form['RID']
    name = form['NAME']
    description = form['DESCRIPTION']
    price = form['PRICE']
    restaurant.add_item(name, description, price, rid)
    dest = f'/menu?id={rid}'
    return redirect(dest)


@app.route("/fixfoodUI", methods=['GET']) 
@login_required
def fixfood():
    reload_db()
    form = request.args
    rid = form['id']
    food_id = form['food_id']
    data = [
        {
            "data":restaurant.get_food(food_id)
        }
    ]
    dest = '/restaurant/fixfoodUI.html'
    return render_template(dest, rid=rid, food_id=food_id, data=data)

@app.route("/fixfood", methods=['GET', 'POST']) 
@login_required
def fix():
    reload_db()
    form = request.form
    rid = form['RID']
    food_id = form['FOOD_ID']
    name = form['NAME']
    description = form['DESCRIPTION']
    price = form['PRICE']
    restaurant.fix_item(name, description, price, food_id)
    dest = f'/menu?id={rid}'
    return redirect(dest)

@app.route("/finish_order", methods=["GET"])
@login_required
def finish_order():
    args = request.args
    cid = args['cid']
    time = args['time']
    rid = session['id']

    restaurant.update_order(cid, time, rid)

    return redirect("/")


@app.route("/menu", methods=['GET', 'POST']) 
@login_required
def menu():
    reload_db() #重新載入資料庫
    if request.method == "GET":
        form = request.args
        rid = form['id']
        if "action" in form and form['action'] == "remove":
            restaurant.remove_item(rid, form['food_id'])

        if session['role'] == 0:
            data = [
                {
                    "name":session['name'],
                    "data":restaurant.get_menu(int(rid)),
                    "rid":rid
                }
            ]
            dest = '/restaurant/menu.html'

        if session['role'] == 2:
            data = [
                {
                    "name":session['name'],
                    "rid":rid,
                    "data":client.get_menu(int(rid)),
                }
            ]
            dest = 'client/menu.html'

    else:
        form = request.form
        order, cid = client.compose_order(form)

        user = init.get_account(session['loginID'])
        now = datetime.now()
   
        for key, value in order.items():
            client.send_order(form['rid'], key, value['quantity'], cid, user[0]['address'], now)
        client.clear_cart(session['id'])

        rid = form['rid']

        dest = 'client/menu.html'
        data = [
                {
                    "name":session['name'],
                    "rid":rid,
                    "data":client.get_menu(int(rid)),
                }
            ]

    
    return render_template(dest, data=data)



@app.route("/cart", methods=['GET', 'POST']) 
@login_required
def cart(): #購物車功能
    reload_db()
    if request.method == "POST":
        form = request.form
        rid = form['rid']

        if form['action'] == "clear":
            client.clear_cart(session['id'])

        elif form['action'] == "remove":
            client.remove_cart(form['food_id'], session['id'])

        elif form['action'] == "add":
                
            food_id = int(form['food_id'])
            quantity = int(form['quantity'])

            now_item = client.get_item(session['id'], food_id)

            if now_item == []:
                client.add_cart(food_id, quantity, session['id'])

            else:
                quantity += now_item[0]['quantity']
                client.update_cart(food_id, quantity, session['id'])

    else:
        args = request.args
        rid = args['rid']
        client.remove_cart(args['food_id'], session['id'])

    data = [
        {"name":session['name'],
         "data":client.get_cart(session['id']),
         "rid":rid,
         "cid":session['id']
        }
             ]

    return render_template("client/cart.html", data=data)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return redirect("register.html")
    
    #处理POST请求（提交注册表单）
    form = request.form
    name = form['NAME']
    mail = form['MAIL']
    pwd = form['PWD']
    address = form['ADDRESS']
    role = form['ROLE']
    
    
    #檢查用戶存在
    user_from_mail = init.check_account(mail, pwd)
    if user_from_mail == []:
        # 如果没有找到，进行注册
        init.register(name, mail, pwd, address, role)
        return redirect("/login.html")  #註冊結束跳轉至登錄界面
    
    return redirect("/register.html")  # 如果註冊失敗，跳回註冊界面

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return redirect("/login.html")
    
    #處理POST请求（提交登录表单）
    form = request.form
    mail = form['MAIL']
    pwd = form['PWD']
    
    #檢查用戶憑據
    user_from_mail = init.check_account(mail, pwd)

    if user_from_mail == []:
        return redirect("/login")
    
   #登錄成功後，保存資料到session
    session['loginID'] = mail
    session['name'] = user_from_mail[0]['name']
    session['id'] = user_from_mail[0]['id']
    session['role'] = user_from_mail[0]['role']
    return redirect("/")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")


@app.route("/submit_feedback", methods=["POST"])
def submit_feedback_form():
    order_id = request.form['order_id']
    rating = int(request.form['rating'])
    feedback = request.form['feedback']
    client.submit_feedback(order_id, rating, feedback)
    return redirect("/")

