from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

def chandl(sock: socket, addr: tuple):
    a = socket(AF_INET, SOCK_STREAM) # setup client socket
    a.connect(('tendhost.ddns.net', 1615))
    sock.settimeout(0)
    a.settimeout(0)
    try:
        while True:
            try: a.send(sock.recv(32768))
            except TimeoutError: pass
            try: sock.send(a.recv(32768))
            except TimeoutError: pass
    except:
        print(f"socket {addr} disconected")

serv = socket(AF_INET, SOCK_STREAM)
serv.bind(('0.0.0.0', 1615))
serv.listen(1024*1024*1024)

while True:
    print("waiting for connection")
    sock, addr = serv.accept()
    print(f"got connection: {addr}")
    print("creating thread")
    th = Thread(target=chandl, args=(sock, addr))
    print("starting it")
    th.start()