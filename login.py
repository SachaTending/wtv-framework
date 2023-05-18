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
wtv-visit: wtv-home:/home
wtv-backgroundmusic-clear: yes
wtv-backgroundmusic-add: wtv-music:/music
"""

@head_waiter.addhandl("login")
def login(data: dict):
    print("requested login, sending wtv-challenge")
    challenge = "".join([choice(list(ascii_lowercase)) for i in range(16)])
    print(f"challenge: {challenge}")
    print(data)
    #return Responce(200, {'wtv-challenge': challenge, 'wtv-visit': 'wtv-head-waiter:/ValidateLogin', 'Content-Type': 'text/html', 'Connection': 'Keep-Alive'})
    return login_data.format(challenge=challenge)
    #return Responce(400, err_data="FUCK YOU")

@head_waiter.addhandl("login-stage-two")
def stage2(data: dict):
    print("stage two login")
    return Responce(200, {'wtv-visit': 'wtv-home:/home'})

@head_waiter.addhandl("ValidateLogin")
def validate_login(data: dict):
    print("GET wtv-head-waiter:/ValidateLogin")
    return Responce(200, {'wtv-visit': 'wtv-home:/splash'})

svcs = [head_waiter]