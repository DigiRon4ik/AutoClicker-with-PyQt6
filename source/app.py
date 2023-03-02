import sys
import time
import threading

from PyQt6 import QtWidgets, QtGui
from MainWindow import Ui_MainWindow
from pynput import mouse, keyboard


class ClickButton():
    def __init__(self, delay, button):
        # super(ClickButton, self).__init__()
        self.delay = delay
        self.button = button
        self.stoping = True
        self.running = False
        self.thr = 0

        self.mmouse = mouse.Controller()
        self.kkeyboard = keyboard.Controller()

    def start(self):
        if self.stoping:
            self.running = True
            self.stoping = False
            self.thr = threading.Thread(target=self.run)
            self.thr.start()

    def stop(self):
        if not self.stoping:
            self.running = False
            self.stoping = True

    def run(self):
        while not self.stoping:
            if type(self.button) == type(mouse.Button.left):
                self.mmouse.click(self.button, 1)
            else:
                self.kkeyboard.tap(self.button)
            time.sleep(self.delay)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.clicker_btn = keyboard.KeyCode(char='5')
        self.switcher_btn = keyboard.Key.f10
        self.delay = 0.15

        self.clicker = ClickButton(self.delay, self.clicker_btn)

        self.tBtnAutoClick.clicked.connect(self.tBtnAutoClick_clicked)
        self.tBtnSwitcher.clicked.connect(self.tBtnSwitcher_clicked)
        self.sldrDelay.valueChanged.connect(self.sldrDelay_valueChanged)
        self.btnSwitcher.clicked.connect(self.btnSwitcher_clicked)

        self.toggle_switcher()

    def toggle_switcher(self):
        def onRelease(key):
            if key == self.switcher_btn:
                self.on_or_off(not self.clicker.running)
        listener = keyboard.Listener(on_release=onRelease)
        listener.start()

    def tBtnAutoClick_clicked(self):
        self.tBtnAutoClick.setText('...')

        def onRelease(key):
            try:
                self.tBtnAutoClick.setText(key.char.upper())
                m_listen.stop()
                self.clicker_btn = key
                self.clicker.button = key
            except AttributeError:
                self.tBtnAutoClick.setText(str(self.clicker_btn).replace(
                    'Button.', '').replace("'", '').upper())
                m_listen.stop()
            return False

        def onClick(x, y, button, pressed):
            self.tBtnAutoClick.setText(
                str(button).replace('Button.', '').upper())
            self.clicker_btn = button
            self.clicker.button = button
            if not pressed:
                k_listen.stop()
                return False

        k_listen = keyboard.Listener(on_release=onRelease)
        k_listen.start()
        m_listen = mouse.Listener(on_click=onClick)
        m_listen.start()

    def tBtnSwitcher_clicked(self):
        self.tBtnSwitcher.setText('...')

        def onRelease(key):
            try:
                self.tBtnSwitcher.setText(str(key).replace(
                    'Key.', '').replace("'", '').upper())
                self.switcher_btn = key
            except AttributeError:
                self.tBtnSwitcher.setText(
                    str(self.switcher_btn).replace('Key.', '').replace("'", '').upper())
            return False
        listener = keyboard.Listener(on_release=onRelease)
        listener.start()

    def sldrDelay_valueChanged(self):
        self.delay = (self.sldrDelay.value() / 10) - 0.05
        self.clicker.delay = self.delay

    def btnSwitcher_clicked(self, cheked):
        self.on_or_off(cheked)

    def on_or_off(self, flag: bool):
        if flag:
            self.tBtnAutoClick.setEnabled(False)
            self.tBtnSwitcher.setEnabled(False)
            self.btnSwitcher.setText('On')
            self.btnSwitcher.setChecked(True)
            self.btnSwitcher.setStyleSheet('color: rgb(0, 255, 0);')
            self.clicker.start()
        else:
            self.tBtnAutoClick.setEnabled(True)
            self.tBtnSwitcher.setEnabled(True)
            self.btnSwitcher.setText('Off')
            self.btnSwitcher.setChecked(False)
            self.btnSwitcher.setStyleSheet('color: rgb(255, 0, 0);')
            self.clicker.stop()


app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('icon.ico'))

window = MainWindow()
window.show()
app.exec()
