import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing

import json
special_token = json.load(open("D:/github/Chatbot_FG/special_token.json"))
special_token

from transformers import ElectraTokenizer

tokenizer = ElectraTokenizer.from_pretrained("monologg/koelectra-base-v3-discriminator") # 전처리 모듈 불러오기
tokenizer.add_special_tokens(special_token)

sequences = []

# 의도 분류 모델 모듈(ELECTRA)
class IntentModel:
    def __init__(self, model_name):

        # 의도 클래스 별 레이블
        self.labels = {0: "메뉴판 요구", 1: "메뉴 검색", 2: "추천메뉴", 3: "결제방법안내", 4: "쿠폰, 포인트",
                       5: "원산지", 6: "시설, 위치", 7: "영업시간", 8: "텀블러", 9: "테이크아웃",
                       10: "주문취소"}

        # 의도 분류 모델 불러오기
        self.model = load_model(model_name)

    def predict_class(self, query):
            # 형태소 분석
            pos = tokenizer.tokenize(query)

            # 문장내 키워드 추출(불용어 제거)
            seq = tokenizer.convert_tokens_to_ids(pos)
            sequences.append(seq)

            # 단어 시퀀스 벡터 크기
            from config.GlobalParams_Electra import MAX_SEQ_LEN

            # 패딩처리
            padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

            predict = self.model.predict(padded_seqs)
            predict_class = tf.math.argmax(predict, axis=1)
            return predict_class.numpy()[0]


