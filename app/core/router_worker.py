from PySide6.QtCore import QObject, Signal, QTimer
from .coords import load_coords
from .screencap import grab_box
from .ocr import ocr_image
from .clicker import focus_window, click, paste_text

class RouterWorker(QObject):
    notice = Signal(str)  # "Для пользователя: ..."
    log = Signal(str)

    def __init__(self, coords_path:str):
        super().__init__()
        self.coords_path = coords_path
        self.coords = load_coords(coords_path)
        self.timer = QTimer()
        self.timer.setInterval(3000)  # каждые 3 сек
        self.timer.timeout.connect(self.scan_for_user_msgs)

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def send_message(self, text:str):
        try:
            wb = self.coords["windowBox"]
            inp = self.coords["input"]
            snd = self.coords["send"]
            focus_window(tuple(wb))
            click(inp["x"], inp["y"], delay_ms=100)
            paste_text(text, typing=False, delay_ms=100)
            click(snd["x"], snd["y"], delay_ms=100)
            self.log.emit("[Router] Sent message")
        except Exception as e:
            self.log.emit(f"[Router] Send failed: {e}")

    def scan_for_user_msgs(self):
        try:
            ans = self.coords["answer"]
            img = grab_box(ans["x"], ans["y"], ans["w"], ans["h"])
            txt = ocr_image(img)
            for line in txt.splitlines():
                if "Для пользователя" in line:
                    self.notice.emit(line.strip())
        except Exception as e:
            self.log.emit(f"[Router] OCR fail: {e}")
