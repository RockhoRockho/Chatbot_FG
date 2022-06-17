import tensorflow as tf

class BertModel():
    def __init__(self, model_name, binarizer):
        
        self.labels = {0: "메뉴판 요구", 1: "주문", 2: "추천메뉴 검색", 3: "결제, 할인, 쿠폰",
                       4: "원산지", 5: "시설 / 위치", 6: "영업시간", 7: "텀블러", 8: "테이크아웃",
                       9: "주문취소"}

        # 의도 분류 모델 불러오기
        self.model = tf.saved_model.load(model_name)

        # 챗봇 Preprocess 객체
        with open(binarizer, 'rb') as f:
            binarizer = pickle.load(f)
        self.p = binarizer

    def predict_intent(self, sentence):
        
        results = tf.nn.softmax(self.model(tf.constant([sentence])))
        intents = self.p.inverse_transform(results.numpy())
        
        return intents[0]