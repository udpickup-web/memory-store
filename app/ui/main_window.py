from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QMessageBox
)
from PySide6.QtCore import Qt, QThread
from ..core.router_worker import RouterWorker
import os

COORDS_ROUTER = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "coords", "router_4k_q1.json"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ClickerBot — Router Interface (No API)")
        self.resize(900, 600)

        root = QWidget()
        lay = QVBoxLayout(root)

        self.input = QTextEdit()
        self.input.setPlaceholderText("Введи сообщение для роутера первого порядка…")
        self.btn_send = QPushButton("Отправить")
        hl = QHBoxLayout()
        hl.addWidget(self.btn_send)

        lay.addWidget(QLabel("Сообщение для роутера:"))
        lay.addWidget(self.input, 1)
        lay.addLayout(hl)

        lay.addWidget(QLabel("Ответы (Для пользователя):"))
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        lay.addWidget(self.output, 1)

        self.setCentralWidget(root)

        self.thread = QThread(self)
        self.worker = RouterWorker(COORDS_ROUTER)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.start)
        self.worker.notice.connect(self._on_notice)
        self.worker.log.connect(self._log)
        self.thread.start()

        self.btn_send.clicked.connect(self._send)

    def closeEvent(self, e):
        try:
            self.worker.stop()
            self.thread.quit()
            self.thread.wait()
        except Exception:
            pass
        return super().closeEvent(e)

    def _send(self):
        text = self.input.toPlainText().strip()
        if not text:
            QMessageBox.information(self, "Пусто", "Введите сообщение.")
            return
        self.worker.send_message(text)

    def _on_notice(self, line:str):
        self.output.append(line)

    def _log(self, line:str):
        self.output.append(line)
