from wtvframework import *
import accounts

reg_svc = Service("wtv-register")

svcs = [reg_svc]

confirm_html = open("pages/wtv-register/confirm.html").read()

@reg_svc.addhandl("register")
def register(data: dict):
    return Responce(200, data=open("pages/wtv-register/register.html").read())

@reg_svc.addhandl("confirm")
def confirm(data: dict):
    return Responce(200, data=confirm_html.format(username=data['options']['username']))

@reg_svc.addhandl("add-user")
def add_user(data: dict):
    accounts.register(data['options']['username'], data['headers']['wtv-client-serial-number'])
    return Responce(200, headers={'wtv-visit': 'wtv-home:/splash'}, data="loading splash...")