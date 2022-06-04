import threading
import json
import datetime

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
        
        word_1 = ['라떼', '커피', '음료', '식사']
        word_2 = ['추천', '인기', '시그니처']
        
        ##################################     DB 초기화    #############################################
        
        if query == 'DB초기화':
            CartItem(db).all_clear_train_data()
            OrderItem(db).all_clear_train_data()
            OrderDetail(db).all_clear_train_data()       
            
            answer = ''
            answer_name = []
            answer_detail = []
            answer_image = []
            intent_predict = 10
            intent_name = ''
            ner_predicts = ''
        
        ##################################     단답처리     #############################################
        
        # word_1 이 들어왔을때 따로 검색단어를 가져옴
        elif query in word_1:
            try:
                p = FindProduct(db)
                answer = p.search(query)
                
                answer_name = []
                answer_detail = []
                answer_image = []
                for i in range(len(answer)):
                    answer_name.append(answer[i]['name'])
                    answer_detail.append(answer[i]['detail'])
                    answer_image.append(answer[i]['image'])
                
                answer = answer_name
                
                intent_predict = 10
                intent_name = '메뉴'
                ner_predicts = ''

            except:
                answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."

        
        # word_2 이 들어왔을때 따로 검색단어를 가져옴
        elif query in word_2:
            try:
                p = FindProduct(db)
                answer = p.search(query)
                
                answer_name = []
                answer_detail = []
                answer_image = []
                for i in range(len(answer)):
                    answer_name.append(answer[i]['name'])
                    answer_detail.append(answer[i]['detail'])
                    answer_image.append(answer[i]['image'])
                
                answer = answer_name
                
                intent_predict = 2
                intent_name = '추천메뉴 검색'
                ner_predicts = ''

            except:
                answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."

         
        # 메뉴판
        elif query == '메뉴판':
            try:
                f = FindAnswer(db)
                answer, answer_image = f.search('메뉴판 요구', None)
                intent_predict = 0
                intent_name = '메뉴판 요구'
                ner_predicts = ''
                
            except:
                answer = "죄송해요 무슨 말인지 모르겠어요"
        
        # 할인, 포인트, 결제
        elif query == '결제':
            with open('pay.txt', 'r', encoding='utf-8') as f:
                answer = f.read()
            answer_image = None
            intent_predict = 3
            intent_name = '결제, 할인, 쿠폰'
            ner_predicts = ''
            
        elif query == '쿠폰':
            with open('coupon.txt', 'r', encoding='utf-8') as f:
                answer = f.read()
            answer_image = 'coupon.png'
            intent_predict = 3
            intent_name = '결제, 할인, 쿠폰'
            ner_predicts = ''
            
        elif query == '할인':
            answer = '할인은 추천메뉴에만 적용됩니다(그 외 메뉴에는 적용되지 않습니다)'
            answer_image = 'coupon.png'
            intent_predict = 3
            intent_name = '결제, 할인, 쿠폰'
            ner_predicts = ''
            
        # 원산지
        elif query == '원산지':
            try:
                f = FindAnswer(db)
                answer, answer_image = f.search('원산지', None)
                intent_predict = 4
                intent_name = '원산지'
                ner_predicts = ''
                
            except:
                answer = "죄송해요 무슨 말인지 모르겠어요"
                    
            
        # 화장실, 와이파이, 매장
        elif query == '화장실' or query == '와이파이' or query == '매장':
            with open('facility.txt', 'r', encoding='utf-8') as f:
                answer = f.read()
            answer_image = None
            intent_predict = 5
            intent_name = '시설 / 위치'
            ner_predicts = ''
            
        # 영업시간
        elif query == '영업시간':
            try:
                f = FindAnswer(db)
                answer, answer_image = f.search('영업시간', None)
                intent_predict = 6
                intent_name = '영업시간'
                ner_predicts = ''
                
            except:
                answer = "죄송해요 무슨 말인지 모르겠어요"
                
        # 개인컵
        elif query == '개인컵':
            try:
                f = FindAnswer(db)
                answer, answer_image = f.search('텀블러', None)
                intent_predict = 7
                intent_name = '텀블러'
                ner_predicts = ''
                
            except:
                answer = "죄송해요 무슨 말인지 모르겠어요"
                
        # 테이크아웃, 테이크 아웃
        elif query == '테이크아웃' or query == '테이크 아웃':
            try:
                f = FindAnswer(db)
                answer, answer_image = f.search('테이크아웃', None)
                intent_predict = 8
                intent_name = '테이크아웃'
                ner_predicts = ''
                
            except:
                answer = "죄송해요 무슨 말인지 모르겠어요"
        
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
                    f = FindAnswer(db)
                    answer_text, answer_image = f.search(intent_name, ner_tags)
                    answer = f.tag_to_word(ner_predicts, answer_text)
                    
                    if intent_predict in [1, 2, 9]:
                        
                        # 개체명 인식되는 것 처리
                        for name, tag in ner_predicts:

                            # B_FOOD일때 상품 추출 
                            if tag == 'B_FOOD':
                                product = name
                                # detail 꺼내기
                                p = FindProduct(db)
                                answer_detail = p.search_detail_from_name(name)
                                answer_image = p.search_image_from_name(name)

                            # B_RECOMMEND일때 해당 상품목록 추출 
                            if tag == 'B_RECOMMEND':
                                recommend = name
                                p = FindProduct(db)
                                
                                # answer 다수값 list로 뽑기
                                answer = p.search(query)
                                for i in range(len(answer)):
                                    answer_name.append(answer[i]['name'])
                                    answer_detail.append(answer[i]['detail'])
                                    answer_image.append(answer[i]['image'])
                                answer = answer_name

                except:
                    answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
                    answer_image = None
    
    
      #####################################       2차 FSM 절차         ###################################
            
            # 주문 후 옵션 값 부터 먼저받음
            elif state == 1:
                
                # 아래값들이 적용안되면 처음으로 가게끔 함
                intent_predict = 0
                intent_name = ''
                ner_predicts = ''
                answer_image = None
                
                # 옵션값으로 숫자값을 받을 때는 입력을 받아 저장
                try:
                    if int(query) > 0 and int(query) <= 8:
                        option = int(query)
                        answer = '''다른 상품을 담고싶다면 <장바구니>를 바로결제를 원하시면 <선택완료>를 입력해주세요 
                        혹여나 옵션수정을 원하시면 해당 옵션번호를 다시 입력해주세요
                        1 = 옵션없음
                        2 = 샷추가
                        3 = 시럽추가
                        4 = 사이즈업
                        5 = 샷 + 시럽추가
                        6 = 샷 + 사이즈업
                        7 = 시럽 + 사이즈업
                        8 = 샷 + 시럽 + 사이즈업
                        '''
                        
                        intent_predict = 1
                        intent_name = '주문'
                        
                except:
                    # intent_predict, product 개체를 받은 상태이다.
                    # 선택지 : 선택완료, 장바구니
                    # 옵션 질문 : 사이즈업, 샷추가, 시럽
                    # 핵심 => ★가격 변동 recv_json_data['Price']
                    # 선택완료 = > 주문 order_list 추가
                    
                    # 선택완료 시 intent_predict 초기화 및 order_list db 추가
                    if query == '선택완료':

                        # 현재시간으로 회원ID를 대체함
                        user_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                        
                        # order_detail db (id, user_id)추가
                        order_detail = OrderDetail(db)
                        order_detail.insert_data(user_id)
                        order_id = order_detail.search_last_id()
                        
                        # cart_item에 데이터 있는지 여부 확인 필요

                        f = FindProduct(db)
                        o = ProductOption(db)
                        order_item = OrderItem(db)
                        cart_item = CartItem(db)
                        # product 이름을 id로 바꾸기
                        if product != 0:
                            product_id = f.search_id_from_name(product)
                        
                        # order_item db (order_id, product_id, option_id, count) insert
                        for i in range(len(cart_item.search_all())):
                            order_item.insert_data(order_id, cart_item.search_all()[i]['product_id'],
                                                   cart_item.search_all()[i]['option_id'], cart_item.search_all()[i]['count']) 

                        # cart_item product + option(price) price 도출      
                        total_price = 0
                        for i in cart_item.search_all():
                            product_price = f.search_price_from_id(i['product_id'])
                            option_price = o.search_price(i['option_id'])
                            total_price += ((product_price + option_price) * i['count'])
                        
                        answer = "주문 총 금액은 {}원 입니다".format(total_price)

                        # cart_item db 제거,  product 초기화
                        product = 0
                        cart_item.all_clear_train_data()


                    # 장바구니 시 장바구니 db 추가 후에 intent_predict = 0 으로 초기화
                    elif query == '장바구니':

                        intent_predict = 0
                        intent_name = ''
                        ner_predicts = ''
                        # db 가져오기
                        order_item = OrderItem(db)
                        cart_item = CartItem(db)

                        
                        # product 이름을 id로 바꾸기
                        product_id = FindProduct(db).search_id_from_name(product)
                        
                        
                        # 바꿀 수량을 가져온다, query는 2번째 질문에 받아온 option 값임
                        
                        #*수정전*count_search = cart_item.search_count(product_id, option)

                        # cart_item db 추가
                        # 있다면 update
                        
                        #*수정전*if count_search:
                        #*수정전*    cart_item.update_data(product_id, option, 1 + count_search)
                        ## 없다면 insert
                        #*수정전*else:
                        #*수정전*    cart_item.insert_data(product_id, option, 1)
                        
                        try:
                            count_search = cart_item.search_count(product_id, option)
                            cart_item.update_data(product_id, option, 1 + count_search)
                        # 없다면 insert
                        
                        except:
                            cart_item.insert_data(product_id, option, 1)
                            

                        # 다른 상품 고를 수 있게 초기화
                        
                        
                        answer = "장바구니에 {}가 담겼습니다".format(product)
                        product = 0
                        
                    else:
                        answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
                        answer_image = None
                        # intent_predict, product 값 초기화
                        intent_predict = 0
                        intent_name = ''
                        ner_predicts = ''
                        product = 0
            
            
            # 할인, 포인트, 결제
            elif state == 3:
                
                intent_predict = 0
                intent_name = ''
                ner_predicts = ''
                
                if query == '결제':
                    with open('pay.txt', 'r', encoding='utf-8') as f:
                        answer = f.read()
                    answer_image = None


                elif query == '쿠폰':
                    with open('coupon.txt', 'r', encoding='utf-8') as f:
                        answer = f.read()
                    answer_image = 'coupon.png'


                elif query == '할인':
                    answer = '할인은 추천메뉴에만 적용됩니다(그 외 메뉴에는 적용되지 않습니다)'
                    answer_image = None
                    
                else:
                    answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
                    answer_image = None
            
            # 주문취소 일때 주문번호도 같이 받은상태임
            elif state == 9:
                
                intent_predict = 0
                intent_name = ''
                ner_predicts = ''
                answer_image = None
                
                # 상품이름이 없을때는 다시 입력하게 함
                if product == 0:
                    answer = "취소하려는 상품을 정확하게 입력해주세요."
                    answer_image = None
                    
                else:
                    if query is None:
                        answer = "주문번호(숫자)를 입력해주세요."
                        intent_predict = 9
                        intent_name = '주문취소'
                        ner_predicts = ''
                    else:
                        # 주문취소 받기위해 intent_predict = 9, 주문 개체명이 보존되어야함
                        # 또한 DB에 order_item에 삭제가 되어야함
                        
                        try:
                            order_id = int(query)
                            f = OrderItem(db)
                            p = FindProduct(db)
                            product_id = p.search_id_from_name(product)
                            f.delete_data(product_id, order_id)
                            answer = "주문번호: {} {}가 취소되었습니다".format(product, order_id)
                            product = 0

                        except:
                            answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
                            answer_image = None
                            product = 0

        
        # 검색된 답변데이터와 함께 앞서 정의한 응답하는 JSON 으로 생성
        send_json_data_str = {
            "Query" : query,
            "Answer" : answer,
            "AnswerImageUrl" : answer_image,
            "Intent" : intent_name,
            "NER" : str(ner_predicts),
            "State" : 0,
            "Product" : 0,
            "Price" : 0,
            "Count" : 1,
            "Option" : 0,
            "Detail" : 0,
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
        elif intent_predict == 10:
            send_json_data_str["Detail"] = answer_detail
        
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


