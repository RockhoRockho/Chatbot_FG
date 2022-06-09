from django.shortcuts import render, redirect
import requests
import pymysql 
import json
from APPS.Login.models import User


DB_HOST = "localhost"
DB_USER = "myuser118"
DB_PASSWORD = "1234"
DB_NAME = "mydb118"

def DatabaseConfig():
    global DB_HOST, DB_USER, DB_PASSWORD, DB_NAME



def chatmain(request):

    return render(request, 'chat_main.html')



def kakaopay(request):
    # 가장최근 order 로 불러옴
    member_id = request.session.get('User')
    user = User.objects.get(user_id=member_id)
    user.id

    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8'
    )
    sql = "SELECT * from order_detail where user_id = {}".format(user.id)

    with db:
        with db.cursor() as cur:
            cur.execute(sql)
            order = cur.fetchone()
    
    order_id = order[0]


    # 유저아이디
    # 리스트 저장
    p_name = []
    p_price = 0
    p_qauntity = 0
    # order 불러오기

    # 장바구니 경로

    #     # 리스트 담기
    sql = "SELECT * from order_item where order_id = {}".format(order_id)
    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8'
    )
    product_id = []
    option_id = []
    with db:
        with db.cursor() as cur:
            cur.execute(sql)
            order_item = cur.fetchall()
            for i in order_item:
                product_id.append(i[2])
                option_id.append(i[3])
                p_qauntity += i[4]

    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8'
    )
    for i in product_id:
        sql = "SELECT name, price from product_cafe where id = {}".format(i)
        with db:
            with db.cursor() as cur:
                cur.execute(sql)
                items = cur.fetchone()
                p_name.append(items[0])
                p_price += items[1]



    if request.method == "POST":    

        url = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + "e0e68565dbf3a2564757105698677a37",   
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  
        }
        params = {
            "cid": "TC0ONETIME",    # 테스트용 코드
            "partner_order_id": order_id,     # 주문번호
            "partner_user_id": member_id,    # 유저 아이디
            "item_name": p_name,        # 구매 물품 이름
            "quantity": p_qauntity,                # 구매 물품 수량
            "total_amount": p_price,        # 구매 물품 가격
            "tax_free_amount": "0",         # 구매 물품 비과세
            "approval_url": "http://127.0.0.1:8000/chatbot/kakaopay/approval/", # 결제 성공시 넘어갈 URL
            "cancel_url": "http://127.0.0.1:8000",  # 결제 취소시 넘어갈 URL
            "fail_url": "http://127.0.0.1:8000", # 결제 실패시 넘어갈 URL
        }

        res = requests.post(url, headers=headers, params=params)
        result = json.loads(res.text)
        request.session['tid'] = result['tid']      # 결제 승인시 사용할 tid를 세션에 저장
        next_url = result['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장

        return redirect(next_url)

    return render(request, 'kakaopay.html')

def approval(request):
    member_id = request.session.get('User')

    # order 불러오기
    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8'
    )
    sql = "SELECT * from order_detail where user_id = {}".format(order_id)

    with db:
        with db.cursor() as cur:
            cur.execute(sql)
            order = cur.fetchone()
    
    order_id = order[0]



    url = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "e0e68565dbf3a2564757105698677a37",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",    # 테스트용 코드
        "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": order_id,     # 주문번호
        "partner_user_id": member_id,    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(url, headers=headers, params=params)
    amount = json.loads(res.text)['amount']['total']
    res = res.json()
    context = {
        'res': res,
        'amount': amount,
    }

    return render(request, 'approval.html', context)