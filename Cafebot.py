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
        query = recv_json_data['Query']
        
        one_word = ['라떼', '커피', '음료', '식사', '추천', '인기', '시그니처']
        
        # one_word 가 들어왔을때 따로 검색단어를 가져옴
        if query in one_word:
            try:
                p = FindProduct(db)
                menu = p.search(query)

            except:
                answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
                answer_image = None
                # state 값 초기화
                state = 0
            
            
        # 할인, 포인트, 결제
        elif query == '결제':
        
            answer = '''
                결제에 관한 설명입니다~~

                1. 결제는 현재 안타깝게도 '카카오페이'로만 결제가 가능합니다. ㅠㅠ
                   혹시나 다른카드로 결제를 원하신다면 현장에 오셔서 결제가능합니다 이점 양해부탁드려요

                2. 결제를 하신 후 상품 수령은 현장에 직접 오셔서 가져가셔야 합니다!(배달이 따로되지 않습니다)

                3. 환불은 고객님이 매장에서 직접 수령해가시기에 이미 결제를 하셨다면 매장을 방문해주시면 
                   상품상태 확인 후 바로 환불처리 해드리겠습니다

                4. 계좌이체는 3333-12-000000 (대표자 : FG) 카카오뱅크로 이체해 주신 후 연락주시면 결제처리 해드리겠습니다!

                혹시나 결제에 관한 의문이 해소가 되지 않으신분들은!
                02-538-0000으로 연락주세요!
            '''
            answer_image = None
            state = 0
            
            
        elif query == '쿠폰':
            
            answer = '''
                쿠폰 관련 설명입니다.

                1. 저희 매장에서 주문하시는 메뉴 수에 따라 쿠폰을 1장씩 발급해드립니다.

                2. 쿠폰을 총 10장 모은 후 결제시에 메뉴에 따라 각기 다른 할인을 받으실 수 있습니다.

                3. 사용하신 쿠폰은 소멸되오니 유의해주시기 바랍니다.

                4. 추가 문의사항이 있으시면 언제든 '02-538-0000'로 연락주시기 바랍니다
            '''
            answer_image = '001.png'
            
            
        elif query == '할인':
            answer = '''
                할인은 추천메뉴에만 적용됩니다(그 외 메뉴에는 적용되지 않습니다)
            '''
            answer_image = None
            state = 0
            
            
        # 화장실, 와이파이, 매장
        elif query == '화장실' or query == '와이파이' or query == '매장':
            answer = '''
                시설 안내입니다
                
                저희 카페 화장실은 정문 우측에 있는 계단으로 올라가서 복도 끝에 있습니다.
                비밀번호: 123456
                
                카페 와이파이
                wifi: cafe_fg_wifi
                비밀번호: 0123456789
                
                매장정보
                이름: 카페 FG
                주소: 736-7 역삼동, 강남구, 서울
                전화번호: 02-538-0000
                오픈 날짜: 2022년 6월 1일
                대표: FG
            '''
            state = 0
        
        # one_word와 관련 없을때
        else:    
            
            # 일반 절차
            # 2차 질문에 해당되지 않을 때는 의도분류, 개체명인식 모델링 진행
            if recv_json_data['State'] == 0:
                # 의도 파악
                intent_predict = intent.predict_class(query)
                intent_name = intent.labels[intent_predict]
                
                # state 값 변경
                state = intent_predict
                
                # 개체명 파악
                ner_predicts = ner.predict(query)
                ner_tags = ner.predict_tags(query)
                    
                # 답변 검색, 분석된 의도와 개체명을 이용해 학습 DB 에서 답변을 검색
                try:
                    f = FindAnswer(db)
                    answer_text, answer_image = f.search(intent_name, ner_tags)
                    answer = f.tag_to_word(ner_predicts, answer_text)
                    
                    # B_FOOD일때 상품 추출 
                    for name, tag in predicts:
                        if tag == 'B_FOOD':
                            product = name
                    

                except:
                    answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
                    answer_image = None

            # 주문메뉴 일때
            elif recv_json_data['State'] == 1:
                
                # 옵션에 대한 질문이 계속 들어옴, 선택완료라고 입력하기 전까지 그전까지 state=1, 개체명 food가 보존되어야함
                # 옵션 질문 : 사이즈업, 샷추가, 시럽
                # 핵심 => ★가격 변동
                # 선택완료 = > 주문 order_list 추가
                
                # state 값 변경
                state = intent_predict
                
                # 선택완료 시 state값 초기화 및 order_list db 추가
                if query == '선택완료':
                    state = 0
                    # order_list db 추가
                    # order_detail db 추가
                    continue
                elif query == '장바구니':
                    #
                    
                else:
                    try:
                        option = ProductOption(db, option_id, product_id)
                        answer_text, answer_image = f.search(intent_name, ner_tags)
                        answer = f.tag_to_word(ner_predicts, answer_text)

                    except:
                        answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
                        answer_image = None

            # 주문취소 일때
            elif recv_json_data['State'] == 9:
                
                # 주문취소 받기위해 State = 9, 주문 개체명이 보존되어야함
                # 또한 DB에 order_item에 삭제가 되어야함
                try:
                    f = FindAnswer(db)
                    answer_text, answer_image = f.search(intent_name, ner_tags)
                    answer = f.tag_to_word(ner_predicts, answer_text)

                except:
                    answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
                    answer_image = None

        
        # 검색된 답변데이터와 함께 앞서 정의한 응답하는 JSON 으로 생성
        send_json_data_str = {
            "Query" : query,
            "Answer" : answer,
            "AnswerImageUrl" : answer_image,
            "Intent" : intent_name,
            "NER" : str(ner_predicts),
            "State" : 0,
            "Product" : 0,
        }
        if menu:
            send_json_data_str['menu'] = menu
        
        # State 값 확인하여 
        if state == 1:
            send_json_data_str["State"] = state
            send_json_data_str["Product"] = product
        elif state == 3:
            send_json_data_str["State"] = state
        elif state == 9:
            send_json_data_str["State"] = state
            send_json_data_str["Product"] = product

            
        

        
        # json 텍스트로 변환. 하여 전송
        message = json.dumps(send_json_data_str)
        conn.send(message.encode())  # utf-8 인코딩하여 클라이언트에 전송
        
        # 메뉴검색 끝났을 때 menu 상태 초기화
        menu = 0

        # 만약 메뉴검색이 끝났을 때 다시 State 초기화
        # if 메뉴검색 끝남:
        #    send_json_data_str["State"] = 0
        
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


