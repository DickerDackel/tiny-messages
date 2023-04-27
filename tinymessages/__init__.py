from queue import Queue, Empty


class Broker:
    """A message broker.  Receivers register a callback function for a list of
    message types they're interested in.  If a message of this type comes in,
    every registered callback will be called with the message as parameter.

    Note, that message types as well as message objects are arbitrary.  message
    types could be An enum, a string, a number, there is no hard definition.

    Same goes for the message.  Objects, strings, tuples, all can be passed as
    a message.

        queue = Queue() broker = Broker(queue)

        class ScoreTable:
            def __init__(self, broker, ...):
                self.broker = broker
                broker.register(self.receiver,
                                [Messages.LOOT_TAKEN,
                                 Messages.ENEMY_DESTROYED,
                                 ...])

            def receiver(self, message_type, message_object):
                if hasattr(message_object, 'points'):
                    self.score += message_object.points

        class Enemy:
            ...
            def die(self):
                self.broker.put(Message.ENEMY_DESTROYED, self)
    """
    def __init__(self, q):
        self.queue = q
        self.receivers = {}

    def register(self, who, what):
        """register another class for a list of message types

            register(callback, [message1, ...])

        After registration, if one of the registered messages is put into the
        queue, the the callback is called with a the message type as well as
        the message object as parameters.
        """
        for message_type in what:
            if message_type not in self.receivers:
                self.receivers[message_type] = []
            self.receivers[message_type].append(who)

    def update(self):
        """Call this every frame to route any passed messages

            broker.update()
        """
        while not self.queue.empty():
            message_type, message = self.queue.get_nowait()
            for receiver in self.receivers[message_type]:
                receiver(message_type, message)

    def put(self, message_type, message):
        """put a message into the queue for distribution.

            broker.put(MESSAGE_TYPE, message)

        This will distribute MESSAGE_TYPE and message to all registered
        callbacks.
        """
        self.queue.put((message_type, message))


class Relay:
    """A message relay.  Receivers with a list of message types and receive as
    result a queue object which they need to read frequently.

    If a message of a registered type type is passed to the relay, it forwards
    this message into the queues of all registered receivers.

    Note, that message types as well as message objects are arbitrary.  message
    types could be An enum, a string, a number, there is no hard definition.

    Same goes for the message.  Objects, strings, tuples, all can be passed as
    a message.

        queue = Queue() broker = Broker(queue)

        class ScoreTable:
            def __init__(self, broker, ...):
                self.broker = broker
                self.queue = broker.register([Messages.LOOT_TAKEN,
                                              Messages.ENEMY_DESTROYED,
                                              ...])

            def update(self, dt):
                while True:
                    try:
                        message_type, message = self.queue.get_nowait()
                    except queue.Empty:
                        break

                    match message_type:
                        case Message.ENEMY_DESTROYED:
                            if hasattr(message, 'points'):
                                self.score += message.points

        class Enemy:
            ...
            def die(self):
                self.broker.put(Message.ENEMY_DESTROYED, self)
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

    def put(self, message_type, message):
        """put a message into the queue for distribution.

            broker.put(MESSAGE_TYPE, message)

        This will distribute MESSAGE_TYPE and message to all registered
        callbacks.
        """
        self.queue.put((message_type, message))
