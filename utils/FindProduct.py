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
    
    # 검색 쿼리 생성
    def _make_query(self, query):
        sql = "select * from product_cafe"

        # 해당 query 목록 전부 고르기
            sql = sql + " where '{}'=1".format(query)

            
            
        return sql       
