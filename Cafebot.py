import threading
import json

from config.DatabaseConfig import *
from utils.Database import Database
from utils.BotServer import BotServer
from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel
from models.ner.NerModel import NerModel
from utils.FindAnswer import FindAnswer
from utils.FindProduct import FindProduct
from utils.ProductOption import ProductOption
from utils.OrderItem import OrderItem
from utils.CartItem import CartItem
from utils.OrderDetail import OrderDetail
from utils.UserCafe import UserCafe

# 전처리 객체 생성
p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
               userdic='utils/train.tsv')

# 의도 파악 모델
intent = IntentModel(model_name='models/intent/best_intent_model.h5', preprocess=p)

# 개체명 인식 모델
ner = NerModel(model_name='models/ner/best_ner_model.h5', preprocess=p)


# 클라이언트 요청을 수행하는 함수 (쓰레드에 담겨 실행될 것임)
def to_client(conn, addr, params):
    db = params['db']
    
    try:
        db.connect()  # DB 연결
        
        # 데이터 수신 (클라이언트로부터 데이터를 받기 위함)
        # conn 은 챗봇 클라이언트 소켓 객체 ( 이 객체를 통해 클라이언트 데이터 주고 받는다 )
        read = conn.recv(2048)  # recv() 는 수신 데이터가 있을 때 까지 블로킹, 최대 2048 바이트만큼 수신
                                # 클라이언트 연결이 끊어지거나 오류발생시 블로킹 해제되고 None 리턴
        print('===========================')
        print('Connection from: %s' % str(addr))
        
        if read is None or not read:
            # 클라이언트 연결이 끊어지거나, 오류가 있는 경우
            print('클라이언트 연결 끊어짐')
            exit(0)  # 종료

            
        # 수신된 데이터(json) 을 파이썬 객체로 변환
        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ", recv_json_data)
        # 값들 받아오기
        query = recv_json_data['Query']
        state = int(recv_json_data['State'])
        product = recv_json_data['Product']
        price = recv_json_data['Price']
        option = recv_json_data['Option']
        detail = recv_json_data['Detail']
        user = recv_json_data['UserId']

        # json data 보내는 값 default
        answer = ''
        answer_name = []
        answer_detail = []
        answer_image = []
        intent_predict = ''
        intent_name = ''
        ner_predicts = ''
        
        # db 연결한 table 세팅
        fa = FindAnswer(db)
        fp = FindProduct(db)
        po = ProductOption(db)
        oi = OrderItem(db)
        od = OrderDetail(db)
        ci = CartItem(db)
        uc = UserCafe(db)
        
        user_id = uc.search_id_from_user_id(user)
        
        
        word_1 = ['라떼', '커피', '음료', '식사']
        word_2 = ['추천', '인기', '시그니처']
        
        ##################################     DB 초기화    #############################################
        
        if query == 'DB초기화':
            ci.all_clear_train_data()
            oi.all_clear_train_data()
            od.all_clear_train_data()   
            answer = '데이터가 초기화 되었습니다'
            
        ##################################     장바구니     #############################################
        
        elif query == '장바구니 비우기' or query == '장바구니비우기':
            ci.all_clear_train_data()
            answer = '장바구니가 비워졌습니다'
            
            
        ################################     주문내역 조회     ##########################################
       
        elif query == '주문내역' or query == '주문내역조회' or query == '주문내역 조회':
            answer = {}
            temp = {}
            for i in od.search_all(user_id):
                for j in oi.search_all_from_orderId(i['id']):
                    if j['order_id'] in answer.keys():
                            answer[j['order_id']].append(fp.search_name_from_id(j['product_id']))
                    else:
                        temp[j['order_id']] = [fp.search_name_from_id(j['product_id'])]
                        answer.update(temp)
            intent_name = '주문내역'

        ##################################     처음으로     #############################################

        elif query == '처음으로':
            answer = ""

            intent_name = '처음으로'
        ##################################     단답처리     #############################################
        
        # word_1 이 들어왔을때 따로 검색단어를 가져옴
        elif query in word_1:
            answer = fp.search(query)

            for i in range(len(answer)):
                answer_name.append(answer[i]['name'])
                answer_detail.append(answer[i]['detail'])
                answer_image.append(answer[i]['image'])

            answer = answer_name
            detail = answer_detail

            intent_predict = 10
            intent_name = '메뉴'
        
        # word_2 이 들어왔을때 따로 검색단어를 가져옴
        elif query in word_2:
            answer = fp.search(query)

            for i in range(len(answer)):
                answer_name.append(answer[i]['name'])
                answer_detail.append(answer[i]['detail'])
                answer_image.append(answer[i]['image'])

            answer = answer_name
            detail = answer_detail

            intent_predict = 2
            intent_name = '추천메뉴 검색'

         
        # 메뉴판
        elif query == '메뉴판':
            answer, answer_image = fa.search('메뉴판 요구', None)
            intent_predict = 0
            intent_name = '메뉴판 요구'
        
        # 할인, 포인트, 결제
        elif query == '결제':
            with open('pay.txt', 'r', encoding='utf-8') as f:
                answer = f.read()
            intent_predict = 3
            intent_name = '결제'
            
        elif query == '쿠폰':
            with open('coupon.txt', 'r', encoding='utf-8') as f:
                answer = f.read()
            answer_image = 'coupon.png'
            intent_predict = 3
            intent_name = '쿠폰'
            
        elif query == '할인':
            answer = '할인은 추천메뉴에만 적용됩니다<br>(그 외 메뉴에는 적용되지 않습니다)'
            answer_image = 'coupon.png'
            intent_predict = 3
            intent_name = '할인'
            
        # 원산지
        elif query == '원산지':
            answer, answer_image = fa.search('원산지', None)
            intent_predict = 4
            intent_name = '원산지'
            
        # 화장실, 와이파이, 매장
        elif query == '화장실' or query == '와이파이' or query == '매장':
            with open('facility.txt', 'r', encoding='utf-8') as f:
                answer = f.read()
            intent_predict = 5
            intent_name = '시설 / 위치'
            
        # 영업시간
        elif query == '영업시간':
            answer, answer_image = fa.search('영업시간', None)
            intent_predict = 6
            intent_name = '영업시간'
                
        # 개인컵
        elif query == '개인컵':
            answer, answer_image = fa.search('텀블러', None)
            intent_predict = 7
            intent_name = '텀블러'

                
        # 테이크아웃, 테이크 아웃
        elif query == '테이크아웃' or query == '테이크 아웃':
            answer, answer_image = fa.search('테이크아웃', None)
            intent_predict = 8
            intent_name = '테이크아웃'
        
        # 선택완료 처리
        elif query == '선택완료':
            
            try:
                # order_detail db (id, user_id)추가
                od.insert_data(user_id)
                order_id = od.search_last_id(user_id)
                
                # product 이름을 id로 바꾸기
                if product != 0:
                    product_id = fp.search_id_from_name(product)
                    ci.insert_data(user_id, product_id, option, 1)
                
                    
                
                # order_item db (order_id, product_id, option_id, count) insert
                for i in range(len(ci.search_all(user_id))):
                    oi.insert_data(order_id, ci.search_all(user_id)[i]['product_id'],
                                           ci.search_all(user_id)[i]['option_id'], ci.search_all(user_id)[i]['count']) 

                # cart_item product + option(price) price 도출      
                total_price = 0
                for i in ci.search_all(user_id):
                    product_price = fp.search_price_from_id(i['product_id'])
                    option_price = po.search_price(i['option_id'])
                    total_price += ((product_price + option_price) * i['count'])
                
                if total_price != 0: 
                    answer = "<div style='margin:15px 0;text-align:left;'><span style='padding:3px 10px;background-color: #386641;color:white;border-radius:3px;'>" +\
                    '주문 총 금액은' + f'{total_price}' +  '원 입니다.<br> 카카오 페이 결제를 진행합니다' +\
                        "</span></div>" + \
                            "<a onclick='openPop()' target='_blank'>" + \
                            "<img id='kakaopay' src='../static/img/kakaopay_icon.png' style='width:98%; height:65px; margin-bottom:3%; border-radius:10px; cursor:pointer;'></a>" + \
                            "<script>$(function(){$(document).ready(function(){$('#kakaopay').hover(function(){$(this).css('border','1px solid white');},function(){$(this).css('border','none');});});})</script>"
                else:
                    answer = '주문을 하시려면 상품을 선택해주셔야 합니다.<br> 메뉴판을 불러오겠습니다<br><br>'
                    intent_predict = 0
                    intent_name = '메뉴판 요구'
                    answer_image = fa.search('메뉴판 요구', None)[1]
                
                price = total_price
                
                # 주문번호는 지금띄우지 않고 카카오페이 결제후에 내역으로 뜨게끔 진행함
                detail = od.search_last_id(user_id)

                # cart_item db 제거,  product 초기화
                product = 0
                ci.all_clear_train_data()
                
            except:
                answer = '판매상품이 아닌 것을 입력하셨거나 올바른 절차가 아닙니다'


        # 장바구니 처리
        elif query == '장바구니':
            
            intent_predict = 0
            intent_name = ''
            ner_predicts = ''
            answer_image = None

            try:
                # product 이름을 id로 바꾸기
                product_id = fp.search_id_from_name(product)

                try:
                    count_search = ci.search_count(user_id, product_id, option)
                    ci.update_data(user_id, product_id, option, 1 + count_search)

                # 없다면 insert
                except:
                    ci.insert_data(user_id, product_id, option, 1)

                option_name = po.option_name(option)
                answer = "장바구니에 '{} - {}'이(가) 담겼습니다".format(product, option_name)
                        
                # 다른 상품 고를 수 있게 초기화
                product = 0
            
            except:
                answer = '판매상품이 아닌 것을 입력하셨거나 올바른 절차가 아닙니다'


        
        # one_word와 관련 없을때
        else:    
        ####################################        일반 절차          ###################################
        
            # 2차 질문에 해당되지 않을 때는 의도분류, 개체명인식 모델링 진행
            if state == 0:
                # 의도 파악
                intent_predict = intent.predict_class(query)
                intent_name = intent.labels[intent_predict]
                
                # 개체명 파악
                ner_predicts = ner.predict(query)
                ner_tags = ner.predict_tags(query)

                # 답변 검색, 분석된 의도와 개체명을 이용해 학습 DB 에서 답변을 검색
                try:
                    answer_text, answer_image = fa.search(intent_name, ner_tags)
                    answer = fa.tag_to_word(ner_predicts, answer_text)
                    
                    if intent_predict in [1, 2, 9]:
                        
                        # 개체명 인식되는 것 처리
                        for name, tag in ner_predicts:

                            # B_FOOD일때 상품 추출 
                            if tag == 'B_FOOD':
                                product = name
                                # detail 꺼내기
                                detail = fp.search_detail_from_name(name)
                                price = fp.search_price_from_name(name)
                                answer_image = fp.search_image_from_name(name)

                            # B_RECOMMEND일때 해당 상품목록 추출 
                            elif tag == 'B_RECOMMEND':
                                product = name

                                # answer 다수값 list로 뽑기
                                rec_list = fp.search(name)

                                answer_image = []
                                for i in range(len(rec_list)):
                                    answer_name.append(rec_list[i]['name'])
                                    answer_detail.append(rec_list[i]['detail'])
                                    answer_image.append(rec_list[i]['image'])
                                answer = answer_name
                                detail = answer_detail

                except:
                    answer = "저희 가게에서 지원되지 않는 제품, 서비스이거나<br> 잘못된 값을 입력하셨습니다"
                    answer_image = None
                    product = 0
    
    
      #####################################       2차 FSM 절차         ###################################
            
            # 주문 후 옵션 값 부터 먼저받음
            elif state == 1:
                
                # 아래값들이 적용안되면 처음으로 가게끔 함
                intent_predict = 0
                intent_name = ''
                ner_predicts = ''
                
                # 옵션값으로 숫자값을 받을 때는 입력을 받아 저장
                try:
                    if int(query) > 0 and int(query) <= 8:
                        option = int(query)
                        answer = '''
                        다른 상품을 담고싶다면 <장바구니>를<br>
                        바로결제를 원하시면 <선택완료>를 입력해주세요<br>
                        옵션수정을 원하시면 해당 옵션번호를 다시 입력해주세요<br><br>
                        
                        커피, 라떼만 해당되는 옵션입니다<br>
                        음료는 사이즈업만 가능합니다.<br>
                        ===========================<br>
                        1 = 옵션없음 (+0원)<br>
                        2 = 샷추가 (+500원)<br>
                        3 = 시럽추가 (+300원)<br>
                        4 = 사이즈업 (+700원)<br>
                        5 = 샷 + 시럽추가 (+800원)<br>
                        6 = 샷 + 사이즈업 (+1200원)<br>
                        7 = 시럽 + 사이즈업 (+1000원)<br>
                        8 = 샷 + 시럽 + 사이즈업 (+1500원)<br>
                        ===========================<br>
                        '''
                        
                        intent_predict = 1
                        intent_name = '주문'
                        
                except:
                    answer = "잘못된 값을 입력하셨습니다.<br> 올바른 절차로 다시 진행해주세요"

                    # intent_predict, product 값 초기화
                    intent_predict = 0
                    product = 0
            
            
            # 할인, 쿠폰, 결제
            elif state == 3:
                answer = "잘못된 값을 입력하셨습니다.<br> 올바른 절차로 다시 진행해주세요"
            
            # 주문취소 일때 주문번호도 같이 받은상태임
            elif state == 9:
                
                # 주문취소 외에 다른 절차를 진행한다면 초기화면으로 돌아가게 하기위한 값
                intent_predict = 0
                
                
                # 상품이름이 없을때는 다시 입력하게 함
                if product == 0:
                    try:
                        check = int(query)
                        answer = "상품명이 입력되지 않았습니다! 상품명을 입력해주세요"
                    except:
                        product = query
                        answer = "주문번호를 입력해주세요"
                    intent_predict = 9
                    intent_name = '주문취소'
                    
                else:
                    try:
                        p = FindProduct(db)
                        
                        order_id = int(query)
                        product_id = fp.search_id_from_name(product)
                        oi.delete_data(product_id, order_id)
                        answer = "주문번호: {} 의 '{}' 가 취소되었습니다".format(query, product)

                        # 혹여나 detail에 연결된 item이 없다면 db 삭제
                        if len(oi.search_all_from_orderId(order_id)) == 0:
                            od.delete_data(query, user_id)

                        # product 초기화
                        product = 0

                    except:
                        answer = '''
                        올바르지 않은 상품명 또는 주문번호입니다.<br>
                        상품명과 주문번호를 확인후에 다시 입력해주세요.
                        '''
                        product = 0

        
        # 검색된 답변데이터와 함께 앞서 정의한 응답하는 JSON 으로 생성
        send_json_data_str = {
            "Query" : query,
            "Answer" : answer,
            "AnswerImageUrl" : answer_image,
            "Intent" : intent_name,
            "NER" : ner_predicts,
            "State" : 0,
            "Product" : 0,
            "Price" : price,
            "Count" : 1,
            "Option" : 1,
            "Detail" : detail,
            "UserId" : user,
        }
        
        # State 값 확인하여 
        if intent_predict == 1:
            send_json_data_str["Product"] = product
            send_json_data_str["Price"] = price
            send_json_data_str["Option"] = option
            send_json_data_str["State"] = int(intent_predict)
        elif intent_predict == 9:
            send_json_data_str["Product"] = product
            send_json_data_str["State"] = int(intent_predict)
        
        # 디버깅
        print(send_json_data_str)
        
        # json 텍스트로 변환. 하여 전송 
        message = json.dumps(send_json_data_str)
        conn.send(message.encode())  # utf-8 인코딩하여 클라이언트에 전송
        
        
        
    except Exception as ex:
        print(ex)
        
    finally:
        if db is not None:  # DB 연결 끊기
            db.close()
        conn.close()  # 클라이언트와의 연결도 끊음
            
    # 함수가 종료되면 쓰레드가 끝남

if __name__ == '__main__':
    # 질문/답변 학습 디비 연결 객체 생성
    db = Database(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
    )
    print("DB 접속")
    
    port = 5050
    listen = 100
    
    # 봇 서버 동작
    bot = BotServer(port, listen)
    bot.create_sock()
    print("cafebot start")
    
    # 무한루프를 돌면서 챗봇 클라이언트의 요청(연결)을 기다린다(리스닝!)
    while True:
        conn, addr = bot.ready_for_client()  # 서버 연결 요청이 서버에서 수락되면, 곧바로 챗봇 클라이언트 서비스 요청 처리하는 쓰레드 생성
        
        params = {
            "db" : db
        }
        client = threading.Thread(target=to_client, args=(
            conn, # 클라이언트 연결 소켓
            addr, # 클라이언트 연결 주소 정보
            params  # 쓰레드 내부에서 DB에 접근할 수 있도록 넘겨줌
        ))
        
        client.start()  # 쓰레드 시작, 위 target 함수가 별도의 쓰레드에 실려 실행된다.


