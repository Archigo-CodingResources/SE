from modules import init, client
from controllers.general import reload_db
from datetime import datetime

def menu(request, session):
    if request.method == "GET":
        form = request.args
        rid = form['id']

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
        
    return dest, data

def cart(request, session):
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
    
    return data

def submit_feedback(request):
    rating = request.form['rating']
    feedback = request.form['feedback']
    rid = request.form['rid']
    client.submit_feedback(rating, feedback, rid)

def show_comment(request):
    form = request.args
    rid = form['id']
    data = client.get_comment(rid)
    return data