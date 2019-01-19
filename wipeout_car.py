from microbit import *
import radio

# SETTINGS

# SETUP
radio.on()

class RadioLatest():
    def __init__(self):
        radio.on()
        self.current_message = None

    def any(self):
        while True:
            message = radio.receive()
            if message:
                self.current_message = message
            else:
                break
        return bool(self.current_message)

    def message_peek(self):
        return self.current_message

    def message_get(self):
        self.any()
        message = self.current_message
        self.current_message = None
        return message
radio_latest = RadioLatest()

# START

display.show(Image.TARGET)

# LOOP
while True:
    if radio_latest.any():
        incoming = radio_latest.message_get()
    else:
        sleep(10)
        continue

    if incoming == 'W':
        display.show(Image.TARGET)
    if incoming == '3':
        display.show(3)
    elif incoming == '2':
        display.show(2)
    elif incoming == '1':
        display.show(1)
    elif incoming == 'S':
        display.show(Image.ARROW_N)
    elif incoming.startswith('F'):
        display.show(Image.SMILE)
