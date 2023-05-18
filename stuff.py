from wtvframework import *

imgs = Service("wtv-images")

svcs = [imgs]

@imgs.addhandl("splash")
def splash_img(data):
    return SendFile("d/splash.gif", ftype="image/gif")