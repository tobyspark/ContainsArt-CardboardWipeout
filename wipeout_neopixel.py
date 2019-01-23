# CARDBOARD WIPEOUT
# http://tobyz.net/projects/wipeout

# Code to run individually-addressable LED strips (WS2812B, aka NeoPixel).
# Used a 5m, 150LED strip, connected on pin 0 via a 3.3v -> 5v line driver chip.
# Two assemblies of PSU, microbit, breakout, and strip were used for the game.

from microbit import *
import neopixel
from radiolatest import RadioLatest

# SETTINGS
strip_length = 150
ticks = 8
forwards = True

# SETUP
strip = neopixel.NeoPixel(pin0, strip_length)
radio_latest = RadioLatest()

def strip_colour(colour):
    '''
    Set the whole LED strip to a single colour. Colour is `(R, G, B)`, 0-255.
    '''
    for position in range(0, strip_length):
        strip[position] = colour
    strip.show()

def countdown_animation(text, colour):
    '''
    Set strip the colour and fade out. Set display to the text.
    Will return if a new message is received over the radio.
    '''
    display.show(text)
    for luma in range(255, 0, -5):
        anim_colour = [min(x, luma) for x in colour]
        for position in range(0, strip_length):
            strip[position] = anim_colour
        strip.show()

        if radio_latest.any():
            return

def clock_generator():
    '''
    Supply the next clock face, forever.
    Needs to be instantiated, to remember where each one of potentially many is in the sequence.
    e.g. `clocks = clock_generator()`
    '''
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
    '''
    Sets a ruler-like tick pattern across the LED strip, and animates a pulse around it.
    The update-rate of the LED slows the more LEDs you update at a time. To go fast,
      this implementation actually only updates the LEDs where the pulse is, leaving
      the tick pattern behind it.
    '''
    tail_length = 10
    if forwards:
        chase_range = (0, strip_length+tail_length)
    else:
        chase_range = (strip_length-1, -tail_length-1, -1)
    while True:
        for chase_position in range(*chase_range):
            display.show(next(clocks))
            for trailing_position in range(0, tail_length+1):
                if forwards:
                    position = chase_position - trailing_position
                else:
                    position = chase_position + trailing_position
                if 0 < position < strip_length:
                    tick_luma = 255 if position % ticks == 0 else 5
                    anim_luma = int(255*((tail_length-trailing_position) / tail_length))
                    strip[position] = (anim_luma, (tick_luma + anim_luma)//2, anim_luma)
            strip.show()
            if radio_latest.any():
                return

# START

display.show(Image.ARROW_N)

# LOOP
while True:
    # Only respond to the latest message received over the radio
    if radio_latest.any():
        incoming = radio_latest.message_get()
    else:
        sleep(10)
        continue

    # State W, for waiting-for-player. Set strips to white, to light the track.
    if incoming == 'W':
        display.show('W')
        strip_colour((255,255,255))
    # State 3, counting down. Red...
    if incoming == '3':
        countdown_animation(3, (255,0,0))
    # State 2, counting down. Red...
    elif incoming == '2':
        countdown_animation(2, (255,0,0))
    # State 1, counting down. Amber...
    elif incoming == '1':
        countdown_animation(1, (255,64,0))
    # State S, for race started. Green! Which the chase animation then wipes across.
    elif incoming == 'S':
        strip_colour((0,255,0))
        chase_animation()
    # State F, for race finish. Blue, why not.
    elif incoming.startswith('F'):
        display.show('F')
        strip_colour((0,0,255))