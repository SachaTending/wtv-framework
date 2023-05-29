from wtvframework import *
from glob import glob
from config import name
from accounts import load_account

home = Service("wtv-home")
favorites = Service("wtv-favorite")
svcs = [home, favorites]
home_data = open("home.html").read()

splash = f"""
<html>
<head>
<display hideoptions nostatus showwhencomplete skipback clearback fontsize=medium>
<title>Engaging wtvframework...</title>
<meta http-equiv=Refresh content="4; url=wtv-home:/Credits-Introduction">
</head>
<body bgcolor="#000000" text="#449944">
<bgsound src="file://ROM/Sounds/Splash.mid">
<center>
<spacer type=block height=88 width=21>
<img src="file://ROM/Images/spacer.gif" height=4><br>
<img src="wtv-images:/splash">
<p>based on TendingStream73's wtv-framework server</p>
<br><br><br>
<p><br>
<p><br>
<table border>
<tr><td>
{name}
<tr><td>Connected: 1 Sixtilion TBit per second/Optical link/Fiber link/Localhost/Direct connection/Built in
</table>
</center>
</body>
</html>"""

@home.addhandl("home")
def index_home(data):
    return Responce(200, data=open("home.html").read().replace('ACCOUNT_NAME_PLACEHOLDER', load_account(data['headers']['wtv-client-serial-number']).name))

@home.addhandl("playlist-load")
def playlist_load(data):
    bgsound_headers = "wtv-backgroundmusic-clear: no_zits\n"
    bgsound_int = 0
    for i in glob("d/BGSound/*"):
        bgsound_int += 1
        bgsound_headers += f"wtv-backgroundmusic-add: wtv-music:/BGSound/{bgsound_int}\n"
    out = f"""200 OK
Content-Type: text/html
Content-Length: 0
{bgsound_headers}
"""
    print(out)
    return out

@home.addhandl("Credits-Introduction")
def creds_intro(data):
    return Responce(200, data=open("pages/wtv-home/Credits-Introduction.html").read())

@home.addhandl("splash")
def splash_handl(data):
    return Responce(200, data=splash)

@favorites.addhandl("favorite")
def favorite_troll(data):
    return Responce(400, err_data="fuck out, you dont have favorites")