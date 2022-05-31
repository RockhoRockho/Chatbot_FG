import socket
import json

# ① 챗봇 엔진 서버 접속 정보
host = "127.0.0.1"  # 챗봇 엔진 서버 IP 주소, IPv4 에선 localhost (자신) 의 주소다
port = 5050  # 챗봇 엔진 서버 통신 포트

# 클라이언트 프로그램 시작
while True:
    query = input("질문 : ")  # 질의 입력
    if(query == "exit"):
        exit(0)
    print('-' * 40)
    
    # 챗봇 엔진 서버 연결 (소켓연결)
    mySocket = socket.socket()
    mySocket.connect((host, port))  # 챗봇 엔진 서버 연결 시도.  실패하면 ConnectionRefusedError 
    
    # 챗봇 엔진 질의 요청
    json_data = {
        "Query": query,
        "BotType": "ProjectFG_Cafe"
    }
    message = json.dumps(json_data)  # json 텍스트로 변경하여
    mySocket.send(message.encode())  # 전송!
    
        
    # 챗봇 엔진으로부터 답변 받아 출력
    data = mySocket.recv(2048).decode()   # 서버로부터 수신 (수신 할때까지 대기, 블로킹)
    ret_data = json.loads(data)           # json -> 파이썬 객체로 변환
    
    # 수신후 답변 출력
    print("답변 : ")
    print(ret_data['Answer'])
    print(ret_data)
    print(type(ret_data))
    print("\n")    
    
    
    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    