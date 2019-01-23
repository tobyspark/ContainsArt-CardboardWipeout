from microbit import radio

class RadioLatest():
    '''
    A only-care-about-the-latest wrapper for the micro:bit radio class.
    Used in http://tobyz.net/projects/wipeout
    '''
    def __init__(self):
        radio.on()
        self.current_message = None

    def any(self):
        '''
        Checks for new messages and returns true if so.
        Can be used to e.g. break out of animation loops
        '''
        while True:
            message = radio.receive()
            if message:
                self.current_message = message
            else:
                break
        return bool(self.current_message)

    def message_peek(self):
        '''
        Returns the current message while keeping it the current message. Message may be None.
        Can be used to e.g. verify the message qualifies to break out of an animation loop
        '''
        return self.current_message

    def message_get(self):
        '''
        Returns and removes the current message. Message may be None
        '''
        self.any()
        message = self.current_message
        self.current_message = None
        return message