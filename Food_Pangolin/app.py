from flask import Flask, render_template, request, session, redirect, flash
from functools import wraps
from controllers import general, restaurant, client, delivery

app = Flask(__name__, static_folder="static", static_url_path="/")
app.config['SECRET_KEY'] = '123TyU%^&'


# 登錄驗證
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        loginID = session.get('loginID')
        if not loginID:
            return redirect('/login')  # 如果沒登錄跳轉至登錄界面
        return f(*args, **kwargs)
    return wrapper

<<<<<<< HEAD
@app.route("/", methods=['GET', 'POST'])
=======
#===========================================================#
#                                                           #
#                            通用                           #
#                                                           #
#===========================================================#

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        status, wrong = general.register(request)
        if status:
            return render_template("/login.html")
        flash(wrong)
    return render_template("/register.html")  # 如果註冊失敗，跳回註冊界面

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("/login.html")
    
    status, wrong = general.login(request)
    
    if not status:
        flash(wrong)
        return render_template("/login.html")
    
    return redirect("/")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")


@app.route("/", methods=['GET', 'POST']) 
>>>>>>> 843f131b1f5a83c465d12c16bf5aed98bcc9928d
@login_required
def homepage():
    if session['role'] >= 0:
        dest, data = general.homepage(session)
    else:
        dest, data = general.homepage_admin(request)
    return render_template(dest, data=data)

@app.route("/menu", methods=['GET', 'POST']) 
@login_required
def menu():
     #重新載入資料庫
    if session['role'] == 0:
        dest, data = restaurant.menu(request, session)

    elif session['role'] == 2: 
        dest, data = client.menu(request, session)
    
    return render_template(dest, data=data)


#===========================================================#
#                                                           #
#                            餐廳                           #
#                                                           #
#===========================================================#



@app.route("/addfoodUI", methods=['GET']) 
@login_required
def addfood():
    
    dest, rid = restaurant.add_foodUI(request)
    return render_template(dest, rid = rid)


@app.route("/addfood", methods=['GET', 'POST']) 
@login_required
def add():
    
    dest = restaurant.add_food(request)
    return redirect(dest)


@app.route("/fixfoodUI", methods=['GET']) 
@login_required
def fixfood():
    
    dest, data, rid, food_id = restaurant.fix_foodUI(request)
    return render_template(dest, rid=rid, food_id=food_id, data=data)

@app.route("/fixfood", methods=['GET', 'POST']) 
@login_required
def fix():
    
    dest = restaurant.fix_food(request)
    return redirect(dest)

@app.route("/finish_order", methods=["GET"])
@login_required
def finish_order():
    restaurant.finish_order(request, session)
    return redirect("/")

<<<<<<< HEAD

@app.route("/menu", methods=['GET', 'POST']) 
@login_required
def menu():
    if session['role'] == 0:
        dest, data = restaurant.menu(request, session)

    elif session['role'] == 2: 
        dest, data = client.menu(request, session)
    
    return render_template(dest, data=data)

=======
#===========================================================#
#                                                           #
#                            客戶                           #
#                                                           #
#===========================================================#
>>>>>>> 843f131b1f5a83c465d12c16bf5aed98bcc9928d


@app.route("/cart", methods=['GET', 'POST']) 
@login_required
def cart(): #購物車功能
    
    data = client.cart(request, session)

    return render_template("client/cart.html", data=data)


@app.route("/order", methods=["POST"])
@login_required
def order_list():
    data = client.get_order(request)
    return render_template("client/order.html", data=data)


@app.route("/feedback", methods=["GET"])
def show_feedback_form():
    data = [{"rid":request.args['rid']}]
    return render_template("/client/feedback.html", data=data)


@app.route("/show_comment",methods=["GET", "POST"])
def show_comment():
    if request.method == "GET":
        rid = request.args['id']

    else:
        client.submit_feedback(request)
        rid = request.form['rid']
    comments = client.show_comment(request)
    data = [
        {
            "rid": rid,
            "data":comments
            }
            ]
    return render_template("/client/comment.html", data=data)


#===========================================================#
#                                                           #
#                           外送員                          #
#                                                           #
#===========================================================#

@app.route("/info", methods=["GET"])
def order_info():
    data = delivery.order_info(request)
    return render_template("/delivery/order_info.html", data=data)

@app.route("/own_order", methods=["GET"])
def own_order_list():
    
    data = delivery.own_order(request, session)

    return render_template("/delivery/own_order_list.html", data=data)

@app.route("/confirm_order", methods=["GET"])
def confirm_order():
    
    delivery.confirm_order(request, session)
    return redirect("/own_order")