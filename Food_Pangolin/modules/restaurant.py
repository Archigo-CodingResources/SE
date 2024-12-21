from modules import init

cursor, conn = init.get_cursor()

def compose_order(cart_data):
    grouped_by_cid = {}
    for item in cart_data:
        cid = item['cid']
        if cid not in grouped_by_cid:
            grouped_by_cid[cid] = []
        grouped_by_cid[cid].append(item)

    grouped_by_cid = list(grouped_by_cid.values())
    
    for items in grouped_by_cid:
        total = 0
        for item in items:
            total += item['price'] * item['quantity']
        items.append(total)

    return grouped_by_cid

def get_order(rid):
    sql = "SELECT * FROM `cart` inner join `food` on cart.food_id = food.food_id where food.rid = %s"
    param = (rid, )
    cursor.execute(sql, param)
    return cursor.fetchall()