from socket import *
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
logger.info("클라이언트 기다리는중...")
serverSock.listen(1)

clientSock, addr = serverSock.accept()
logger.info("클라이언트 찾음")

logger.info("서버 시작됨!")
while True:
    try:
        recvData = json.loads(clientSock.recv(1024).decode())
        logger.info(f"{recvData[0]} 플래이어가 움직임 현재 좌표 : {recvData[1]}")
        clientSock.send(json.dumps(recvData).encode('utf-8'))
    except Exception as err:
        logger.info(f"연결이 끊기거나 오류가 발생함! {err}")
        break