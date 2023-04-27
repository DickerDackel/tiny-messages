from tinymessages import Broker
from time import time, sleep
from enum import Enum, auto
from queue import Queue, Empty
from random import random


class MessageType(Enum):
    SCORE_INCREASED = auto()
    SOMETHING_DIED = auto()
    ...


class Score:
    def __init__(self, broker):
        self.score = 0
        self.broker = broker
        self.broker.register(self.receiver,
                             [MessageType.SOMETHING_DIED])

    def receiver(self, message_type, message):
        match message_type:
            case MessageType.SOMETHING_DIED:
                if hasattr(message, 'points'):
                    self.score += message.points
                    print(f'{self}: score increased by {message.points} to {self.score}')
                else:
                    print(f'{self}: score not increased, since entity provides no points')

                self.broker.queue.put((MessageType.SCORE_INCREASED, self.score))


class Loot:
    def __init__(self, broker):
        self.broker = broker
        self.points = 42

    def die(self):
        self.broker.queue.put((MessageType.SOMETHING_DIED, self))


class BigBrother:
    def __init__(self, broker):
        self.broker = broker
        self.broker.register(self.receiver,
                             [MessageType.SOMETHING_DIED,
                              MessageType.SCORE_INCREASED])

    def receiver(self, message_type, message):
        match message_type:
            case MessageType.SOMETHING_DIED:
                print(f'{self} Yeeaaahhiiii, somebody died!')

            case MessageType.SCORE_INCREASED:
                print(f'{self} Yeeaaahhiiii, we scored!')

            case MessageType.REGISTER:
                print(f'{self}: I notice, that {message[0]} has registered {message[1]}')


def main():
    queue = Queue()

    print("Message broker demo:")
    broker = Broker(queue)
    bigbrother = BigBrother(broker)
    score = Score(broker)
    loot = Loot(broker)

    # run for 30 seconds, there's a 1/3 chance, that loot is dropped.
    t0 = time()
    while time() - t0 < 30:
        print('Tick!')
        broker.update()
        if random() < 0.3:
            loot.die()
        sleep(1)
