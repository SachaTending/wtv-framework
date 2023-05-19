from wtvframework import *
from random import choice
from string import ascii_lowercase
head_waiter = Service("wtv-head-waiter")

login_data = """200 Error: Operation was succesful
Connection: Keep-Alive
Expires: Wed, 09 Oct 1991 22:00:00 GMT
wtv-country: US
wtv-challenge: {challenge}
wtv-language-header: en-US,en
wtv-visit: wtv-head-waiter:/ValidateLogin
wtv-backgroundmusic-clear: yes
wtv-backgroundmusic-add: wtv-music:/music
"""

splash_data = """
<html>
<head>
<display hideoptions nostatus showwhencomplete skipback clearback fontsize=medium>
<title>Engaging wtvframework...</title>
<meta http-equiv=Refresh content="1; url=wtv-home:/home">
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

@head_waiter.addhandl("login")
def login(data: dict):
    print("requested login, sending wtv-challenge")
    challenge = "".join([choice(list(ascii_lowercase)) for i in range(16)])
    print(f"challenge: {challenge}")
    print(data)
    #return Responce(200, {'wtv-challenge': challenge, 'wtv-visit': 'wtv-head-waiter:/ValidateLogin', 'Content-Type': 'text/html', 'Connection': 'Keep-Alive'})
    return login_data.format(challenge=challenge)

@head_waiter.addhandl("login-stage-two")
def stage2(data: dict):
    print("stage two login")
    return Responce(200, {'wtv-visit': 'wtv-home:/home'})

validate_login_headers = {
    'wtv-visit': 'wtv-home:/splash',
}

@head_waiter.addhandl("ValidateLogin")
def validate_login(data: dict):
    print(f"challenge: {data['headers'].get('wtv-challenge')}")
    #return Responce(200, {'wtv-visit': 'wtv-head-waiter:/splash'})
    return Responce(200, validate_login_headers)

@head_waiter.addhandl("splash")
def splash(data: dict):
    return Responce(200, data=splash_data)

svcs = [head_waiter]