# CARDBOARD WIPEOUT
# http://tobyz.net/projects/wipeout

# Code to run the game from a micro:bit board.
#
# BUTTON A to start race
# BUTTON B to finish race
# Optionally - beam break sensor to finish race
#
# Broadcast states are W, 3, 2, 1, S, F
# F also messages the race time, in whole seconds.

from microbit import *
import radio

use_beam_break = False

def change_state(state, message=None):
    '''
    Register the change of state with everything that needs it
    '''
    # The control micro:bit's display
    display.show(state)
    # All other micro:bits nearby
    radio.send(state)
    # Anything connected via serial, e.g. computer for sounds and projection
    if message:
        print('{}{}'.format(state, message))
    else:
        print(state)

def get_beam_watcher():
    '''
    Returns a function that will report on whether the beam is broken.
    Need to instantiate that function, e.g. `beam_watcher = get_beam_watcher()`
    Requires a LED beam breaker pair, the sensor installed on pin0.
    I found reading the input directly wasn't reliable, this returns True if 
      it has been true in the last 1/4 second.
    '''
    last_state = None
    last_time = running_time()

    def beam_watcher():
        state = pin0.read_digital()
        time = running_time()
        if state is False and last_state is True:
            if time - last_time < 250:
                return True
        last_state = state
        last_time = time
        return state

    return beam_watcher
beam_watcher = get_beam_watcher()

radio.on()

# Times are milliseconds since the micro:bit was powered on.
race_start_time = 0
race_end_time = 0

# STATE: Initial: Wait for player
change_state('W')
# RUN...
while True:
    if button_a.was_pressed():
        # STATE: Countdown
        for state in ['3', '2', '1']:
            change_state(state)
            sleep(1500)
        # STATE: Race start
        change_state('S')
        race_start_time = running_time()
        # STATE: Race running
        while not button_b.was_pressed():
            # Start detecting the car over the line
            # once it's had a chance to leave the line
            if use_beam_break:
                if running_time() - race_start_time > 5*1000:
                    if not beam_watcher():  # beam broken
                        break
            pass
        race_end_time = running_time()
        # STATE: Race end
        change_state('F', (race_end_time - race_start_time)//1000)
        sleep(5*1000)
        # STATE: Wait for player
        button_a.was_pressed()  # clear any extra button presses
        button_b.was_pressed()
        change_state('W')
