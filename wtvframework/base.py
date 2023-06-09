from . import parsehttp
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from os import path
default_headers = {
    "Content-Type": "text/html",
}
resp_table = {
    # 100 - 199
    "100": "Continue",
    "101": "Switching Protocols",
    "102": "Processing",
    "103": "Early Hints",
    # 200 - 299
    "200": "OK",
    "201": "Created",
    "202": "Accepted",
    # webtv dont need too much respone codes
    # 300 - 399
    "300": "Multiple Choices",
    "301": "Moved Permanentry",
    "302": "Found",
    "303": "See Other",
    # 400 - END
    "400": "Server ran into problem." # WebTV Creates alert based on awk: 400 {alert_text}
}

class Responce:
    def __init__(self, code: int=204, headers: dict=default_headers, data: str="", err_data: str="Server ran into problem.", content_type: str="text/html"):
        self.code = code
        self.data = data
        self.headers = headers
        self.err_data = err_data
        self.headers['Content-Type'] = content_type
    def pack(self) -> str:
        if self.code == 400:
            code_data = self.err_data
        else:
            code_data = resp_table[str(self.code)]
        data = f"{self.code} {code_data}"
        data += "\n"
        # Start to write headers
        #if self.headers.get("Content-Length", "NO VALUE") == "NO VALUE": self.headers['Content-Length'] = str(len(self.data))
        self.headers['Content-Length'] = str(len(self.data))
        for i in self.headers:
            data += f"{i}: {self.headers[i]}\n"
        # Add data
        data += f"\n{self.data}"
        # End of packing, return out data
        return data

class SendFile:
    def __init__(self, file: str=None, headers: dict=default_headers, ftype: str="application/octet-stream"):
        self.file = file
        self.headers = headers
        #if self.headers.get("Content-Length", "NO VALUE") == "NO VALUE": self.headers['Content-Length'] = str(stat(file).st_size)
        self.headers['Content-Type'] = ftype
        #self.headers['Content-Type'] = 'application/octet-stream'
    def pack_header(self) -> str:
        data = f"200 OK\n"
        # Add headers
        if self.headers.get("Content-Length", "NO VALUE") == "NO VALUE": self.headers['Content-Length'] = str(path.getsize(self.file))
        for i in self.headers:
            data += f"{i}: {self.headers[i]}\n"
        # Add newline for data
        data += "\n"
        # End of packing headers, return out data
        return data

class Service:
    def __init__(self, service: str="wtv-1800"):
        self.name = service
        self.handlers = {}
        self.files: dict[str, SendFile] = {}
    def addhandl(self, name):
        def addh(handler):
            self.handlers[name] = handler
        return addh
    def addfile(self, handl, sfile: SendFile):
        self.files[handl] = sfile

class Minisrv:
    def __init__(self, name: str="server"):
        self.name = name
        self.services: list[Service] = []
    def addservice(self, srv: Service):
        self.services.append(srv)
    def handle_thread(self, sock: socket, addr: tuple):
        try:
            out = self.handle(sock.recv(32768))
            if isinstance(out, Responce): out = out.pack().encode()
            if isinstance(out, SendFile):
                out.headers['Content-Length'] = str(path.getsize(out.file))
                sock.send(out.pack_header().encode())
                file = open(out.file, "rb")
                bs = path.getsize(out.file)
                st = 0
                while bs > st:
                    sock.send(file.read(1024))
                    st+=1024
            else:
                sock.send(out)
        except Exception as e:
            print(f"{addr}: exception: {e}")
            sock.send(f"400 WTVFramework ran into problem: {e}\r\nContent-length: 0\r\nContent-Type: text/html\r\n".encode())
        sock.close()
    def handle(self, data: bytes):
        data: dict[str, str] = parsehttp(data.decode())
        # Determine request type(HTTP Or WTVP?)
        if ":/" in data['url']:
            service = data['url'].split(":",1)[0]
            handl = data['url'].split(":/",1)[1]
            for i in self.services:
                if i.name == service:
                    for a in i.handlers:
                        if a == handl:
                            print(f"{data['type']} {data['url']}")
                            outdata: str = i.handlers[a](data)
                            if isinstance(outdata, str): outdata = outdata.encode()
                            return outdata
            # If handler not found, try to lookup for files in each service
            for i in self.services:
                if i.name == service:
                    for a in i.files:
                        if a == handl:
                            print(f"{data['type']} {data['url']}: FILE")
                            return i.files[a] # Send SendFile class
            print(f"{data['type']} {data['url']}: NOT FOUND")
            return f"400 WTVFramework ran into problem, error: URL {data['url']} not found\r\nContent-length: 0\r\nContent-Type: text/html\r\n".encode()
        else:
            print("Request handler: Detected HTTP request")
            return "HTTP/1.1 418 I'm a teapot\r\nContent-Type: text/html\r\nContent-Length: {len}\r\nServer: wtv-framework/1.0\r\n\n<p>I cannot make coffee for you because im a teapot</p>".format(len=len("<p>I cannot make coffee for you because im a teapot</p>")).encode()
    def runserv(self, host: str='localhost', port: int=1615, maxlisten: int=15):
        print("services: ", end="")
        for i in self.services:
            print(i.name, "", end="")
        print()
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(maxlisten)
        print("ready")
        while True:
            try: sock, addr = self.sock.accept()
            except KeyboardInterrupt:
                print("shutting down")
                self.sock.close()
                exit()
            th = Thread(target=self.handle_thread, name=f"Handler({addr})", args=(sock, addr))
            th.start()
            