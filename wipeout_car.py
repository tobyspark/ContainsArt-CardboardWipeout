from microbit import *
from radiolatest import RadioLatest

# SETTINGS

# SETUP
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
