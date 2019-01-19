# Add your Python code here. E.g.
from microbit import *
import neopixel
import radio

strip_length = 150
ticks = 8
strip = neopixel.NeoPixel(pin0, strip_length)
incoming_interrupt = None

def strip_colour(colour):
    for position in range(0, strip_length):
        strip[position] = colour
    strip.show()

def countdown_animation(text, colour):
    display.show(text)
    for luma in range(255, 0, -5):
        anim_colour = [min(x, luma) for x in colour]
        for position in range(0, strip_length):
            strip[position] = anim_colour
        strip.show()

        global incoming_interrupt
        incoming_interrupt = radio.receive()
        if incoming_interrupt:
            return

def clock_generator():
    while True:
        yield Image.CLOCK12
        yield Image.CLOCK1
        yield Image.CLOCK2
        yield Image.CLOCK3
        yield Image.CLOCK4
        yield Image.CLOCK5
        yield Image.CLOCK6
        yield Image.CLOCK7
        yield Image.CLOCK8
        yield Image.CLOCK9
        yield Image.CLOCK10
        yield Image.CLOCK11
clocks = clock_generator()

def chase_animation():
    tail_length = 20
    while True:
        for chase_position in range(0, strip_length+tail_length):
            display.show(next(clocks))
            for trailing_position in range(0, tail_length+1):
                position = chase_position - trailing_position
                if position < strip_length:
                    tick_luma = 255 if position % ticks == 0 else 5
                    anim_luma = int(255*((tail_length-trailing_position) / tail_length))
                    strip[position] = (anim_luma, (tick_luma + anim_luma)//2, anim_luma)
            strip.show()

            global incoming_interrupt
            incoming_interrupt = radio.receive()
            if incoming_interrupt:
                return

radio.on()
messages = ['3', '2', '1', 'Go']

display.show(Image.ARROW_N)
while True:
    if incoming_interrupt:
        incoming = incoming_interrupt
        incoming_interrupt = None
    else:
        incoming = radio.receive()
    if incoming is None:
        sleep(10)
        continue

    if incoming == 'W':
        display.show('W')
        strip_colour((255,255,255))
    if incoming == '3':
        countdown_animation(3, (255,0,0))
    elif incoming == '2':
        countdown_animation(2, (255,0,0))
    elif incoming == '1':
        countdown_animation(1, (255,64,0))
    elif incoming == 'S':
        strip_colour((0,255,0))
        chase_animation()
    elif incoming.startswith('F'):
        display.show('F')
        strip_colour((0,0,255))

