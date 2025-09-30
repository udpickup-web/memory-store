import mss
from PIL import Image

def grab_box(x:int, y:int, w:int, h:int):
    with mss.mss() as s:
        monitor = {"left": x, "top": y, "width": w, "height": h}
        sct = s.grab(monitor)
        img = Image.frombytes("RGB", sct.size, sct.rgb)
        return img
