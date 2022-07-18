# 프로젝트명 : FG Cafe

## 개요
**챗봇을 활용한 비대면 카페 문의, 주문, 결제 서비스 웹사이트 입니다.**  

### 기간 : 2022.05.20 ~ 2022.06.17

### 팀명 : Project FG

### 팀원 : 

   이준영(조장) : 전체 총괄 및 담당,  ner_train_data 구축, 의도분류 모델 및 개체명 인식모델 구축

   유원준 : 사용자 사전 구축, 데이터전처리, 서비스 프론트 페이지 구축, Intent_train_data 구축

   정연교 : Bert 모델구축, Model 조사(CNN, Bi-LSTM), FSM 구축

   김두원 : 클라이언트 서버, Intent_train_data 구축, 챗봇 엔진 구축, 서비스 프론트 페이지 구축 

   공동작업 : 데이터 수집, 추출, 생성 및 전처리

### 사용기술 : 
   1) 데이터 : corpus, 단어사전, 의도분류 모델, 개체명 인식 모델 등 자체 데이터 생성
   2) 개발 환경 : Jupyter Notebook, VS code, Sqlite3, MySQL
   3) 개발 언어 : Python, Javascript, HTML, CSS
   4) 개발 라이브러리 : Django, Flask, Transformer, Tensorflow, Pandas

## Intent Train Data + 단어사전
  * **Intent, NER 학습을 위한 데이터 (약 1만1천개)**
     > AI Hub 카페 대화 데이터셋  
       Sentence 약 7천개  
       불필요한 Sentence 제거 + 구체적 Sentence 추가  
       중심 단어와 단어 어미에 따른 분류  
       카페 관련 단어 및 대화로 데이터 구성   

  * **단어사전 구축**
    > 단어 사전 : 카페 메뉴  
      train_data : 카페 대화  
      label : 의도   
      Tokenizer : Komoran, BertWordpieceTokenizer  
      Word : 약 1만개  
<img>
