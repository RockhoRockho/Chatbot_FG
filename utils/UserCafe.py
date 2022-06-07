class UserCafe():
    
    def __init__(self, db):
        self.db = db
        
    
    def all_clear_train_data(self):
        # 기존 학습 데이터 삭제
        sql = '''
                delete from user_cafe
            '''
        self.db.execute(sql)

        # auto increment 초기화
        sql = '''
        ALTER TABLE user_cafe
        '''
        self.db.execute(sql)
        
    
    def search_id_from_user_id(self, user_id):
        sql = "select id from user_cafe where user_id = '{}'".format(user_id)
        usercafe = self.db.select_one(sql)
        pk = usercafe['id']
        
        return pk
        
