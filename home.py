from wtvframework import *

home = Service("wtv-home")

home_data = open("home.html").read()

splash = """
<!--- *=* Copyright 1996-99 WebTV Networks, Inc. All rights reserved. --->
<html>
<head>
<display hideoptions nostatus showwhencomplete skipback clearback fontsize=medium>
<title>Engaging wtvframework...</title>
<meta http-equiv=Refresh content="4; url=wtv-home:/home?">
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
    return Responce(200, data=home_data)

@home.addhandl("splash")
def splash_handl(data):
    return Responce(200, data=splash)