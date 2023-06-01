from glob import glob

import config
from wtvframework import *
from rendertext import render, render_autosize

imgs = Service("wtv-images")
content_svc = Service("wtv-content")
wtv_center_svc = Service("wtv-center")
favorite_svc = Service("wtv-favorite")
star_svc = Service("wtv-star")
svcs = [imgs, content_svc, wtv_center_svc, favorite_svc, star_svc]

@imgs.addhandl("splash")
def splash_img(data):
    return SendFile("d/splash.gif", ftype="image/gif", headers={'Refresh': '4; url=wtv-home:/home'})

@imgs.addhandl("text")
def text_test(data):
    data2 = render_autosize("тест, rendered with pillow :)")
    header = f"""200 OK
Content-Type: image/jpeg
Content-Length: {len(data2)}


""".encode()
    header+=data2
    return header

# wtv-center stuff
@wtv_center_svc.addhandl("money")
def money_handl(data):
    return Responce(200, data=open("pages/wtv-center/money.html").read())

# wtv-star
@star_svc.addhandl("star")
def star_handl(data):
    return Responce(200, data=open("pages/wtv-star/star.html").read().replace("NETWOK_NAME_PLACEHOLDER", config.name))

# Add ROMCache
for i in glob("d/content/ROMCache/*"): content_svc.addfile(i.removeprefix("d/content/"), SendFile(i))
for i in glob("d/content/ad/*"): content_svc.addfile(i.removeprefix("d/content/"), SendFile(i))