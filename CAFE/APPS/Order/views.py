from django.shortcuts import render
import pymysql 

# DB 가져오기
DB_HOST = "localhost"
DB_USER = "myuser118"
DB_PASSWORD = "1234"
DB_NAME = "mydb118"

db = None

db = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            db=DB_NAME,
            charset='utf8'
        )

sql = ''' 
    SELECT * from order_detail
'''
dtl_li = []
with db.cursor() as cur:
    cur.execute(sql)
    order_detail = cur.fetchall()

for i in order_detail:
    pk, _ = i
    dtl_li.append(pk)

sql = ''' 
    SELECT * from product_cafe
'''

with db.cursor() as cur:
    cur.execute(sql)
    product = cur.fetchall()

prd_dic = {}
for i in product:
    pk, name, _, _, _, _, _, _, _, _ = i
    prd_dic[pk] = name

sql = ''' 
SELECT * from product_option
'''
with db.cursor() as cur:
    cur.execute(sql)
    option = cur.fetchall()

opt_dic = {}
for i in option:
    pk, _, opt_name = i
    opt_dic[pk] = opt_name

sql = ''' 
SELECT * from order_item
'''

with db.cursor() as cur:
    cur.execute(sql)
    order_item = cur.fetchall()


list = []
for i in order_item:
    pk, order_id, product_id, option_id, count = i
    list.append([order_id, prd_dic[product_id], opt_dic[option_id], count])

db.close()

def order_list(request):
    context = {
        "orders" : list,
    }
    return render(request, 'order_list.html', context)