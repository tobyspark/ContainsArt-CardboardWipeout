from microbit import *
import radio

radio.on()

while True:
    incoming = radio.receive()
