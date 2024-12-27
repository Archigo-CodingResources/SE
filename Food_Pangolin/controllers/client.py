from modules import init, client
from controllers.general import reload_db
from datetime import datetime

def menu(request, session):
    reload_db() #重新加載DB，確保DB資料最新
    if request.method == "GET":
        form = request.args
        rid = form['id']

        data = [
            {
                "name":session['name'],
                "rid":rid,
                "data":client.get_menu(int(rid)), #從client獲取menu
            }
        ]
        dest = 'client/menu.html'

    else: #如果是POST，代表用戶提交了訂單
        form = request.form 
        order, cid = client.compose_order(form)

        user = init.check_account(session['loginID']) #查詢用戶資料
        now = datetime.now()
   
        for key, value in order.items():
            client.send_order(form['rid'], key, value['quantity'], cid, user[0]['address'], now)
        client.clear_cart(session['id']) #cart清空

        rid = form['rid']

        dest = 'client/menu.html'
        data = [
                {
                    "name":session['name'],
                    "rid":rid,
                    "data":client.get_menu(int(rid)),
                }
            ]
        
    return dest, data

def cart(request, session):
    reload_db()
    if request.method == "POST":
        form = request.form
        rid = form['rid']

        if form['action'] == "clear": #清空
            client.clear_cart(session['id'])

        elif form['action'] == "remove": #移除
            client.remove_cart(form['food_id'], session['id'])

        elif form['action'] == "add": #增加
                
            food_id = int(form['food_id'])
            quantity = int(form['quantity'])

            now_item = client.get_item(session['id'], food_id)

            if now_item == []:
                client.add_cart(food_id, quantity, session['id']) #如果沒有該資料，添加進cart

            else:
                quantity += now_item[0]['quantity'] #如果有，資料+1
                client.update_cart(food_id, quantity, session['id'])

    else: # 如果是GET請求，表示用戶查看購物車
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
    
    return data

def submit_feedback(request):
    rating = request.form['rating']
    feedback = request.form['feedback']
    rid = request.form['rid']
    print(request.form)
    client.submit_feedback(rating, feedback, rid)

def show_comment(request):
    reload_db()
    form = request.args
    rid = form['id']
    data = client.get_comment(rid)
    return data
