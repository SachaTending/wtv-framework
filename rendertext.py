from PIL import Image, ImageDraw, ImageMode, ImageFont
from os.path import abspath
from io import BytesIO
debug: print
def debug(*a, **b):
    print(*a, **b)

def render_autosize(text: str) -> bytes:
    # One glyph' size is 14x32
    return render(text, [int(ImageFont.truetype(abspath("Roboto-Light.ttf"), size=30).getlength(text)), 32])

def render(text: str, size: tuple[int, int]=[14, 32], fontsize: int=30) -> bytes:
    debug("creating image")
    img: Image.Image = Image.new("RGB", size=size)
    debug("loading font")
    font = ImageFont.truetype(abspath("Roboto-Light.ttf"), size=fontsize)
    draw = ImageDraw.Draw(img)
    debug("drawing text")
    draw.text((0, 0), text, font=font)
    debug("creating buffer")
    temp = BytesIO()
    debug("writing to buffer")
    img.save(temp, format="jpeg")
    temp.seek(0)
    debug("all done")
    return temp.read()