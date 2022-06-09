from django.shortcuts import render
from utils.Product import Product
from utils.OrderDetail import OrderDetail
from utils.OrderItem import OrderItem
from utils.ProductOption import ProductOption

dtl_li = []
for i in OrderDetail():
    pk, _ = i
    dtl_li.append(pk)

prd_dic = {}
for i in Product():
    pk, name, price, _, _, _, _, _, _, _ = i
    prd_dic[pk] = [name, price]

opt_dic = {}
for i in ProductOption():
    pk, _, opt_name = i
    opt_dic[pk] = opt_name

list = []
for i in OrderItem():
    pk, order_id, product_id, option_id, count = i
    list.append([order_id, prd_dic[product_id], opt_dic[option_id], count])

print(list)

def order_list(request):
    return render(request, 'order_list.html')