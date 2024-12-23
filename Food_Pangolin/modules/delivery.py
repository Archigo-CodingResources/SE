from modules import init

cursor, conn = init.get_cursor()

def compose_order(cart_data):
    grouped_by_cid_time = {}

    # 按 (cid, time) 分组
    for item in cart_data:
        key = (item['cid'], item['time'])  # 使用 (cid, time) 作为分组键
        if key not in grouped_by_cid_time:
            grouped_by_cid_time[key] = []
        grouped_by_cid_time[key].append(item)

    # 将分组结果转换为列表
    grouped_by_cid_time = list(grouped_by_cid_time.values())

    return grouped_by_cid_time

def get_order():
    sql = "SELECT the_order.oid, the_order.cid, the_order.time, rid as r_id, name as r_name, account.address as r_addr, the_order.address as c_addr from the_order inner join account on the_order.rid = account.id;"
    cursor.execute(sql)
    return cursor.fetchall()

