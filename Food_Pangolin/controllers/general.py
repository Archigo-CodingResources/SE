from modules import init, client, restaurant, delivery
from importlib import reload
from app import session

def reload_db():
    reload(init)
    reload(restaurant)
    reload(client)
    reload(delivery)

def register(request):
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
        return True  #註冊結束跳轉至登錄界面
    
    return False

def login(request):
    #處理POST请求（提交登录表单）
    form = request.form
    mail = form['MAIL']
    pwd = form['PWD']
    
    #檢查用戶憑據
    user_from_mail = init.check_account(mail, pwd)

    if user_from_mail == []:
        return False, None
    
   #登錄成功後，保存資料到session
    session['loginID'] = mail
    session['name'] = user_from_mail[0]['name']
    session['id'] = user_from_mail[0]['id']
    session['role'] = user_from_mail[0]['role']
    return True, session


def homepage(session):
    if session['role'] == 0:
        cart = restaurant.get_order(int(session['id']))
        cart_data = restaurant.compose_order(cart)

        data = [
            {
                "name":session['name'],
                "data":cart_data
                }
            ]
        
        dest = '/restaurant/order.html'
        
    elif session['role'] == 1:
        order = delivery.get_order()
        order_data = delivery.compose_order(order)

        data = [{
            "name":session['name'],
            "data":order_data
            }]
        
        dest = "delivery/order_list.html"

    elif session['role'] == 2:
        data = [{
            "name":session['name'],
            "data":client.get_restaurant()
            }]
        
        dest = 'client/restaurant.html'

    return dest, data

def homepage_admin(request, session):
    dest = '/platform/summary.html'

    args = request.args
    data =[{}]

    if args:   
        role = args['type']
        data = init.get_summary(role)

    return dest, data

def menu(request):
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