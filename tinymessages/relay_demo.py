from tinymessages import Relay
from time import time, sleep
from enum import Enum, auto
from queue import Queue, Empty
from random import random


class MessageType(Enum):
    SCORE_INCREASED = auto()
    SOMETHING_DIED = auto()
    ...


class Score:
    def __init__(self, relay):
        self.score = 0
        self.relay = relay
        self.queue = self.relay.register([MessageType.SOMETHING_DIED])

    def update(self):
        print(f'Score: {self.queue.empty()}')
        while True:
            try:
                message_type, message = self.queue.get_nowait()
                print(f'Score fetched {message_type}, {message}')
            except Empty:
                print('Score: Nothing')
                break
            print(f'{self}: Received {message_type}: {message}')
            match message_type:
                case MessageType.SOMETHING_DIED:
                    if hasattr(message, 'points'):
                        self.score += message.points
                        print(f'{self}: score increased by {message.points} to {self.score}')
                    else:
                        print(f'{self}: score not increased, since entity provides no points')

                        self.relay.queue.put((MessageType.SCORE_INCREASED, self.score))


class Loot:
    def __init__(self, relay):
        self.relay = relay
        self.points = 42

    def die(self):
        self.relay.queue.put((MessageType.SOMETHING_DIED, self))

    def update(self):
        ...


class BigBrother:
    def __init__(self, relay):
        self.relay = relay
        self.queue = self.relay.register([MessageType.SOMETHING_DIED,
                                          MessageType.SCORE_INCREASED])

    def update(self):
        while True:
            try:
                message_type, message = self.queue.get_nowait()
            except Empty:
                break
            match message_type:
                case MessageType.SOMETHING_DIED:
                    print(f'{self} Yeeaaahhiiii, somebody died!')

                case MessageType.SCORE_INCREASED:
                    print(f'{self} Yeeaaahhiiii, we scored!')


def main():
    queue = Queue()

    print("Relay demo:")
    relay = Relay(queue)
    bigbrother = BigBrother(relay)
    score = Score(relay)
    loot = Loot(relay)

    # run for 30 seconds, there's a 1/3 chance, that loot is dropped.
    t0 = time()
    while time() - t0 < 30:
        print('Tick!')
        relay.update()
        if random() < 0.3:
            loot.die()

        bigbrother.update()
        loot.update()
        score.update()
        sleep(1)
