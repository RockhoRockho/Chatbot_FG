from django.shortcuts import render
import pymysql 
from utils.Product import Product

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
    SELECT * from order_item
'''
with db.cursor() as cur:
    cur.execute(sql)
    order_item = cur.fetchall()

product_dic = {}
for i in product:
    pk, name, _, _, _, _, _, _, _, _ = i
    product_dic[pk] = name


    opt_dic = {}
    for i in option:
        pk, _, opt_name = i
        opt_dic[pk] = opt_name


def order_list(request):
    return render(request, 'order_list.html')