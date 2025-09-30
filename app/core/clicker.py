import time, pyautogui as pag, pyperclip
from typing import Tuple

def click(x:int, y:int, delay_ms:int=0):
    if delay_ms: time.sleep(delay_ms/1000.0)
    pag.click(x=x, y=y)

def paste_text(text:str, typing=False, delay_ms:int=0):
    if delay_ms: time.sleep(delay_ms/1000.0)
    if typing:
        pag.write(text, interval=0.01)
    else:
        pyperclip.copy(text)
        pag.hotkey("ctrl","v")

def focus_window(window_box:Tuple[int,int,int,int]):
    x,y,w,h = window_box
    pag.click(x + 10, y + 10)  # фокус верхнего-левого угла окна
