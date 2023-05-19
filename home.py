from wtvframework import *
from glob import glob

home = Service("wtv-home")

home_data = open("home.html").read()

splash = """
<html>
<head>
<display hideoptions nostatus showwhencomplete skipback clearback fontsize=medium>
<title>Engaging wtvframework...</title>
<meta http-equiv=Refresh content="4; url=wtv-home:/home">
</head>
<body bgcolor="#000000" text="#449944">
<bgsound src="file://ROM/Sounds/Splash.mid">
<center>
<spacer type=block height=88 width=21>
<img src="file://ROM/Images/spacer.gif" height=4><br>
<img src="wtv-images:/splash">
<br><br><br>
<p><br>
<p><br>
<table border>
<tr><td>
wtvframework v0.1
<tr><td>Connected: 1 TBit per second/Optical link
</table>
</center>
</body>
</html>"""

@home.addhandl("home")
def index_home(data):
    return Responce(200, data=open("home.html").read())

@home.addhandl("playlist-load")
def playlist_load(data):
    bgsound_headers = "wtv-backgroundmusic-clear: no_zits\n"
    bgsound_int = 0
    for i in glob("d/BGSound/*"):
        bgsound_int += 1
        bgsound_headers += f"wtv-backgroundmusic-add: wtv-music/BGSound/{bgsound_int}\n"
    out = f"""200 OK
{bgsound_headers}Content-Type: text/html\nContent-Length: 0
\n"""
    return out

@home.addhandl("splash")
def splash_handl(data):
    return Responce(200, data=splash)