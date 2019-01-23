# CARDBOARD WIPEOUT

Code to run _Cardboard Wipeout_, an immersive racing game that riffs off the seminal (to me) futuristic video game _[wipE'out”](https://en.wikipedia.org/wiki/Wipeout_2097)_. Developed in a workshop for the youth of Somerset, UK.

Full description and video: http://tobyz.net/projects/wipeout

Coding note – During the workshop, sometimes the race would finish straight after starting, or after the `finish` state pass straight through `waiting-for-player` into `countdown`. The problem is the radio module has a queue of incoming messages, which meant stale or even dropped messages. So here’s my only-care-about-the-latest wrapper class, developed and tested afterwards –

```
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
```

– which allows you to break out of e.g. animation loops if a message is received –

```
if radio_latest.any():
    return
```

– and your main loop can then be –

```
while True:
    if radio_latest.any():
        incoming = radio_latest.message_get()
    else:
        sleep(10)
        continue

    if incoming == ...
        ...
```