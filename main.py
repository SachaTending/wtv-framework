from wtvframework import parsehttp, Minisrv, Service, Responce, SendFile
import home, login, sys, stuff
from config import *

print("starting server")
m = Minisrv()
svc = Service()

xd_data = """
<h1>amogus</h1>
<a href=\"wtv-brazil:/u-going-to-brazil\">brazil</a>
<a href=\"wtv-1800:/music\">music</a>
"""

def wtv_svcs_add():
    out = ""
    sheet = "wtv-service: name={name} host=185.252.146.160 port=1615 flags={flags}" 
    for i in m.services:
        if i.name.startswith(('wtv-1800', 'wtv-star')):
            out += sheet.format(name=i.name, flags="0x00000012")
        else:
            out += sheet.format(name=i.name, flags="0x00000007")
        if i.name == "wtv-1800": out += " connections=15892659828057"
        out += "\n"
    return out


@svc.addhandl("xd")
def b(data):
    return Responce(200, data=xd_data)

@svc.addhandl("preregister_old")
def a(data):
    return """200 OK
Connection: Keep-Alive
wtv-initial-key: BCK9Zzas8So=
Content-Type: text/html
wtv-backgroundmusic-clear: no_zits
wtv-backgroundmusic-add: wtv-music:/BGSound/1
wtv-client-time-zone: GMT -0000
wtv-client-time-dst-rule: GMT
wtv-client-date: Fri, 28 Apr 2023 19:12:37 GMT
Content-length: 0
wtv-visit: wtv-head-waiter:/ValidateLogin
wtv-service: reset
wtv-service: name=wtv-1800 host=127.0.0.1 port=1615 flags=0x00000012 connections=214723987234985
wtv-service: name=wtv-star host=127.0.0.1 port=1615 flags=0x00000012
wtv-service: name=wtv-music host=127.0.0.1 port=1615 flags=0x00000007
wtv-service: name=wtv-head-waiter host=127.0.0.1 port=1615 flags=0x00000007
wtv-service: name=wtv-home host=127.0.0.1 port=1615 flags=0x00000012
wtv-service: name=wtv-images host=127.0.0.1 port=1615 flags=0x00000007
wtv-service: name=wtv-* host=127.0.0.1 port=1615 flags=0x00000007
wtv-home: wtv-home:/home
\n"""

@svc.addhandl("preregister")
def preregister(data):
    return f"""200 OK
Connection: Keep-Alive
wtv-initial-key: BCK9Zzas8So=
Content-Type: text/html
wtv-client-time-zone: GMT -0000
wtv-client-time-dst-rule: GMT
wtv-client-date: Fri, 28 Apr 2023 19:12:37 GMT
Content-length: 0
wtv-backgroundmusic-load-playlist: wtv-home:/playlist-load
wtv-visit: wtv-head-waiter:/ValidateLogin
wtv-service: reset
wtv-home: wtv-home:/home
{wtv_svcs_add()}
"""

svc2 = Service("wtv-brazil")
musicsvc = Service("wtv-music")

brazil = """
<h1>u going to brazil</h1>
<h1>fun fact: webtv can open any service</h1>
"""

@svc2.addhandl("u-going-to-brazil")
def c(data):
    return Responce(400, err_data="U GOING TO BRASIL NOW")

@musicsvc.addhandl("music")
def music(data):
    return SendFile("d/music.mp3", ftype="audio/mpeg")

@musicsvc.addhandl("BGSound/1")
def bgsound_1(data):
    return SendFile("d/BGSound/KarTV.mid", ftype="audio/midi")

svc3 = Service("NON-WTV-XD".lower())
data2 = """
<h1>non wtv service xd</h1>"""
@svc3.addhandl("")
def nonwtv(data):
    return """200 OK
Content-Type: text/html
Content-Length: {len}
\n
{data}
""".format(len=len(data2), data=data2)

# Add services
m.addservice(svc)
m.addservice(svc2)
m.addservice(svc3)
m.addservice(home.home)
for i in login.svcs: m.addservice(i)
for i in stuff.svcs: m.addservice(i)
m.addservice(musicsvc)
#print(f"wtv_svcs_add: {wtv_svcs_add()}")
m.runserv(host=host, port=port)

# client:ConfirmConnectSetup?serviceType=custom&machine=127.0.0.1&port=1615&useEncryption=true&connect=Connect