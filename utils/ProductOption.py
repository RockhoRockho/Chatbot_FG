# 학습 데이터 초기화

class ProductOption():
    
    def __init__(self, db):
        self.db = db
        
    
    def all_clear_train_data(self):
        # 기존 학습 데이터 삭제
        sql = '''
                delete from product_option
            '''
        self.db.execute(sql)


        # auto increment 초기화
        sql = '''
        ALTER TABLE product_option
        '''
        self.db.execute(sql)
    
    def search_price(self, option_id):
        sql = "select price from product_option where id = {}".format(option_id)
        option_price = self.db.select_one(sql)
        return option_price['price']


    def option_name(self, option_id):
        sql = "select option_name from product_option where id = {}".format(option_id)
        option_name = self.db.select_one(sql)
        return option_name['option_name']