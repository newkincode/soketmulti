from socket import *
from threading import Thread
import json
import log4py

logger = log4py.Logger()

settingfile = open('server_config.json', 'r')
setting = json.loads(settingfile.read())
settingfile.close()
del settingfile

print(f"ip = {setting['ip']}\nport = {setting['port']}\nip가 0.0.0.0으로 나오는게 정상입니다")

logger.info("서버 소켓 생성중...")
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind((setting['ip'], setting['port']))
serverSock.listen()

logger.info("서버 시작됨!")

try:
    def work(clientSock: socket, addr):
        data = json.loads(clientSock.recv(1024).decode())
        logger.debug(data)
        if setting["game"] == data[0]:
            nick = data[1]
            logger.info(f"{nick} 플래이어가 접속함!")
            while True:
                try:
                    recvData = json.loads(clientSock.recv(1024).decode())
                    logger.info(f"{nick} 플래이어가 움직임 현재 좌표 : {recvData}")
                    # 수정: 클라이언트로부터 받은 데이터를 다시 해당 클라이언트로 전송
                    clientSock.send(json.dumps(recvData).encode('utf-8'))
                except Exception as err:
                    logger.error(f"연결이 끊기거나 오류가 발생함! {err}")
                    break
        else:
            logger.error(f"클라이언트가 접속을 시도했으나 버전이 달라 접속에 실패함")
        # 수정: 해당 클라이언트와의 연결 종료
        clientSock.close()

    try:
        while True:
            clientSock, addr = serverSock.accept()
            t = Thread(target=work, args=(clientSock, addr))
            t.start()
    except Exception as err:
        logger.error(f"서버가 종료되거나 오류가 발생함! {err}")
except:
    serverSock.close()

# 서버 소켓 닫기
serverSock.close()
