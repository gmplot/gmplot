import os
import base64
import cStringIO

from PIL import Image
from PIL.ImageColor import getcolor, getrgb
from PIL.ImageOps import grayscale

MASK = 'FFFFFF.png'

def marker_tint(tint='#ffffff'):
    dir = os.path.dirname(__file__)
    src = os.path.join(dir, MASK)

    src = Image.open(src)
    src.load()

    tr, tg, tb = getrgb(tint)
    tl = getcolor(tint, "L")
    if not tl: tl = 1
    tl = float(tl)
    sr, sg, sb = map(lambda tv: tv/tl, (tr, tg, tb)) 

    luts = (tuple(map(lambda lr: int(lr*sr + 0.5), range(256))) +
            tuple(map(lambda lg: int(lg*sg + 0.5), range(256))) +
            tuple(map(lambda lb: int(lb*sb + 0.5), range(256))))
    l = grayscale(src)
    if Image.getmodebands(src.mode) < 4:
        merge_args = (src.mode, (l, l, l))
    else:
        a = Image.new("L", src.size)
        a.putdata(src.getdata(3))
        merge_args = (src.mode, (l, l, l, a))
        luts += tuple(range(256))

    return Image.merge(*merge_args).point(luts)

def marker_base64(color='ffffff'):
    # questions/29332424/python-3-changing-colour-of-an-image/29379704#29379704
    image = marker_tint("#" + color)
    image_buffer = cStringIO.StringIO()
    image.save(image_buffer, format="PNG")
    return base64.b64encode(image_buffer.getvalue())
