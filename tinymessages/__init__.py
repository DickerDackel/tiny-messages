from queue import Queue, Empty


class Broker:
    """A message broker.  Receivers register a callback function for a list of
    message types they're interested in.  If a message of this type comes in,
    every registered callback will be called with the message as parameter.
    """
    def __init__(self, q):
        self.queue = q
        self.receivers = {}

    def register(self, who, what):
        for message_type in what:
            if message_type not in self.receivers:
                self.receivers[message_type] = []
            self.receivers[message_type].append(who)

    def update(self):
        while not self.queue.empty():
            message_type, message = self.queue.get_nowait()
            for receiver in self.receivers[message_type]:
                receiver(message_type, message)


class Relay:
    """A message relay.  Receivers get back a set of queues that they can fetch
    their messages from.

    This requires active polling on the receiver's side, e.g. in the update method.
    """
    def __init__(self, q):
        self.queue = q
        self.receivers = {}
        self.has_queue = {}

    def register(self, what):
        queue = Queue()
        for message_type in what:
            if message_type not in self.receivers:
                self.receivers[message_type] = []
            self.receivers[message_type].append(queue)
            print(f'somebody registered {message_type} with {queue}')

        return queue

    def update(self):
        while True:
            try:
                message_type, message = self.queue.get_nowait()
            except Empty:
                break
            for queue in self.receivers[message_type]:
                queue.put((message_type, message))
                print(f'put {message_type}, {message} to {queue}')
