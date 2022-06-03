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

## Global
intent_predict = 0
intent_name = ''
ner_predicts = ''
answer = ''
answer_image = ''

def set_intent_values(predict, name, ner):
    global intent_predict
    intent_predict = predict
    global intent_name
    intent_name = name
    global ner_predicts
    ner_predicts = ner
    
def answer_short(db, query):
    global answer
    global answer_image
    global intent_predict
    
    word_0 = ['메뉴판']
    word_2 = ['추천', '인기', '시그니처']
    word_3 = ['결제', '쿠폰', '할인']
    word_4 = ['원산지']
    word_5 = ['화장실', '와이파이', '매장']
    word_6 = ['영업시간']
    word_7 = ['개인컵']
    word_8 = ['테이크아웃', '테이크 아웃']
    word_10 = ['라떼', '커피', '음료', '식사']

    question = word_0 + word_2 + word_3 + word_4 + word_5 + word_6 + word_7 + word_8 + word_10
    
    if query in question:
        try:
            ## Word 0
            if query in word_0:
                f = FindAnswer(db)
                answer, answer_image = f.search('메뉴판 요구', None)
                set_intent_values(0, '메뉴판 요구', '')
                
            ## Word 2
            elif query in word_2:
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
                
                set_intent_values(2, '추천메뉴 검색', '')
                
            ## Word 3
            elif query in word_3:
                with open('coupon.txt', 'r', encoding='utf-8') as f:
                    answer = f.read()
                if query == '쿠폰':
                    answer_image = '001.png'
                else:
                    answer_image = None
                set_intent_values(3, '결제, 할인, 쿠폰', '')
                
            ## Word 4
            elif query in word_4:
                f = FindAnswer(db)
                answer, answer_image = f.search('원산지', None)
                set_intent_values(4, '원산지', '')
                
            ## Word 5
            elif query in word_5:
                with open('facility.txt', 'r', encoding='utf-8') as f:
                    answer = f.read()
                answer_image = None
                set_intent_values(5, '시설 / 위치', '')
                                
            ## Word 6
            elif query in word_6:
                f = FindAnswer(db)
                answer, answer_image = f.search('영업시간', None)
                set_intent_values(6, '영업시간', '')
                                
            ## Word 7
            elif query in word_7:
                f = FindAnswer(db)
                answer, answer_image = f.search('텀블러', None)
                set_intent_values(7, '텀블러', '')
                                
            ## Word 8
            elif query in word_8:
                f = FindAnswer(db)
                answer, answer_image = f.search('테이크아웃', None)
                set_intent_values(8, '테이크아웃', '')
                
            ## Word 10
            elif query in word_10:
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
                
                set_intent_values(10, '메뉴', '')
        except:
            answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
            answer_image = None
            
        return answer
    else:
        set_intent_values(404, 'Error', '')
        answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
        return answer
            
def to_client(conn, addr, params):
    db = params['db']
    
    try:
        db.connect()
        
        read = conn.recv(2048)
        
        print('===========================')
        print('Connection from: %s' % str(addr))
        
        if read is None or not read:
            print('Client disconnected')
            exit(0)  # 종료

        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ", recv_json_data)
        # 값들 받아오기
        query = recv_json_data['Query']
        state = recv_json_data['State']
        product = recv_json_data['Product']
        price = recv_json_data['Price']
        option = recv_json_data['Option']
        
        print(answer_short(db, query));

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
        if db is not None:
            db.close()
        conn.close()
        
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