

from modules import restaurant
from controllers.general import reload_db


def menu(request, session):
    if request.method == "GET":
        form = request.args
        rid = form['id']
        if "action" in form and form['action'] == "remove":
            restaurant.remove_item(rid, form['food_id'])

        data = [
            {
                "name":session['name'],
                "data":restaurant.get_menu(int(rid)),
                "rid":rid
                }
                ]
        dest = '/restaurant/menu.html'

    return dest, data

def add_foodUI(request):
    form = request.args
    rid = form['id']
    dest = '/restaurant/addfoodUI.html'

    return dest, rid

def add_food(request):
    form = request.form
    rid = form['RID']
    name = form['NAME']
    description = form['DESCRIPTION']
    price = form['PRICE']
    restaurant.add_item(name, description, price, rid)
    dest = f'/menu?id={rid}'

    return dest

def fix_foodUI(request):
    form = request.args
    rid = form['id']
    food_id = form['food_id']
    data = [{"data":restaurant.get_food(food_id)}]
    dest = '/restaurant/fixfoodUI.html'

    return dest, data, rid, food_id

def fix_food(request):
    form = request.form
    rid = form['RID']
    food_id = form['FOOD_ID']
    name = form['NAME']
    description = form['DESCRIPTION']
    price = form['PRICE']
    restaurant.fix_item(name, description, price, food_id)
    dest = f'/menu?id={rid}'

    return dest

def finish_order(request, session):
    args = request.args
    cid = args['cid']
    time = args['time']
    rid = session['id']

    restaurant.update_order(cid, time, rid)