class EventSample(object):

    def __init__(self):
        self.callbacks = None

    def on(self, event_handler, callback):
        if self.callbacks is None:
            self.callbacks = {}

        if event_handler not in self.callbacks:
            self.callbacks[event_handler] = [callback]
            pass
        else:
            self.callbacks[event_handler].append(callback)

    def trigger(self, event_handler):
        if self.callbacks is not None and event_handler in self.callbacks:
            for callback in self.callbacks[event_handler]:
                callback(self)


class MClass(EventSample):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return "Message from other class: " + repr(self.message)


def echo(text):
    print(text)


MC = MClass("Sample text")
MC.on("sample_event", echo)
MC.trigger("sample_event")
