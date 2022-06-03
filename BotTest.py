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
    
def answer_short(db):
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

    if query:
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
            
def to_client(conn, addr, params):
    db = params['db']
    
    try:
        db.connect()
        
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
        
        answer_short(db);
        
    except Exception as ex:
        print(ex)
        
    finally:
        if db is not None:
            db.close()
        conn.close()