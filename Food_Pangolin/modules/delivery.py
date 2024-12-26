from modules import init

cursor, conn = init.get_cursor()

def compose_order(cart_data):
    grouped_by_cid_time = {}

    # 按顧客id(cid)和訂單時間(time) 分組
    for item in cart_data:
        key = (item['cid'], item['time'])  #使用(cid, time)作為分組健
        if key not in grouped_by_cid_time:
            grouped_by_cid_time[key] = []
        grouped_by_cid_time[key].append(item)

    # 将分組结果轉換為列表
    grouped_by_cid_time = list(grouped_by_cid_time.values())

    order_num = 1
    for orderlist in grouped_by_cid_time: #將訂單編號加入分組結果
        orderlist.append(order_num)
        order_num += 1

    return grouped_by_cid_time

#合併訂單信息
def merge_order_info(orders):
    total = 0
    for order in orders:
        if isinstance(order, int): #遇到訂單編號時結束計算
            break

        total += order['price'] * order['quantity']

    return orders, total

#獲取尚未被外送員接單的訂單列表
def get_order():
    sql = "SELECT the_order.oid, the_order.cid, the_order.time, rid as r_id, name as r_name, account.address as r_addr, the_order.address as c_addr, the_order.status from the_order inner join account on the_order.rid = account.id where the_order.did is NULL;"
    cursor.execute(sql)
    return cursor.fetchall()

#獲取訂單的詳細信息
def get_order_info():
    sql = "SELECT the_order.oid, the_order.cid, the_order.did, the_order.time, food.name, food.price, the_order.quantity, the_order.quantity * food.price as total, the_order.rid as r_id, account.name as r_name, account.address as r_addr, the_order.address as c_addr, the_order.status from the_order inner join account on the_order.rid = account.id inner join food on food.food_id = the_order.food_id where the_order.did is NULL"
    cursor.execute(sql)
    return cursor.fetchall()

#獲取外送員自己負責的訂單詳情
def get_own_order_info(did):
    sql = "SELECT the_order.oid, the_order.cid, the_order.did, the_order.time, food.name, food.price, the_order.quantity, the_order.quantity * food.price as total, the_order.rid as r_id, account.name as r_name, account.address as r_addr, the_order.address as c_addr, the_order.status from the_order inner join account on the_order.rid = account.id inner join food on food.food_id = the_order.food_id WHERE the_order.did = %s and the_order.status < 3"
    param = (did, )
    cursor.execute(sql, param)
    return cursor.fetchall()

#獲取外送員自己負責的訂單列表
def get_own_order(id):
    sql = "SELECT the_order.oid, the_order.cid, the_order.time, rid as r_id, name as r_name, account.address as r_addr, the_order.address as c_addr, the_order.status from the_order inner join account on the_order.rid = account.id where the_order.status < 3 and did = %s"
    param = (id, )
    cursor.execute(sql, param)
    return cursor.fetchall()

#外送員認領的訂單
def claim_order(did, cid, time):
    sql = "UPDATE `the_order` SET `did`= %s WHERE cid = %s and time = %s"
    param = (did, cid, time, )
    cursor.execute(sql, param)
    conn.commit()
    return

#確認訂單完成
def confirm_order(did, cid, time, total, rid):
    #更新訂單狀態為完成 (status = 3)
    sql = "UPDATE `the_order` SET `status`= 3 WHERE did = %s and cid = %s and time = %s"
    param = (did, cid, time, )
    cursor.execute(sql, param)
    conn.commit()
    
    sql = "UPDATE `account` SET `summary` = `summary` + %s WHERE id = %s"
    param = (total, cid, )
    cursor.execute(sql, param)
    conn.commit()

    sql = "UPDATE `account` SET `summary` = `summary` + %s WHERE id = %s"
    param = (total, rid, )
    cursor.execute(sql, param)
    conn.commit()

    sql = "UPDATE `account` SET `summary` = `summary` + 1 WHERE id = %s"
    param = (did, )
    cursor.execute(sql, param)
    conn.commit()
    return
