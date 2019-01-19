from microbit import *
import radio

def change_state(state, message=None):
    display.show(state)
    radio.send(state)
    if message:
        print('{}{}'.format(state, message))
    else:
        print(state)

def get_beam_watcher():
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
            if running_time() - race_start_time > 5*1000:
                if not beam_watcher():  # beam broken
                    break
        race_end_time = running_time()
        # STATE: Race end
        change_state('F', (race_end_time - race_start_time)//1000)
        sleep(5*1000)
        # STATE: Wait for player
        change_state('W')