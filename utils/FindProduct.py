class FindProduct:
    
    # Database 인스턴스 객체로 생성
    def __init__(self, db):
        self.db = db    # 이 객체를 통해 답변을 검색
        
    # 답변 검색
    def search(self, query):  
        # 질문내용 (query)으로 답변 검색
        sql = self._make_query(query)
        answer = self.db.select_all(sql)
            
        return answer
    
    def search_id(self, name):
        sql = "select id from product_cafe where name = '{}'".format(name)
        product_id = self.db.select_one(sql)
        return product_id
    
    # 검색 쿼리 생성
    def _make_query(self, query):
        sql = "select * from product_cafe"

        # 해당 query 목록 전부 고르기
        if query == '라떼' or query == '커피' or query == '음료' or query == '식사':
            sql = sql + " where '{}'=1".format(query)
            
        # 추천 목록 대상은 따로 db에 따라 적용
        elif query == '시그니처':
            sql = sql + " where recommend = 1".format(query)
        elif query == '인기':
            sql = sql + " where recommend = 2".format(query)
        elif query == '추천':
            sql = sql + " where recommend = 3".format(query)
            
            
        return sql       
