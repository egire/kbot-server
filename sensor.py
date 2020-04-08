import queue, threading
#import RPi.GPIO as GPIO


class sensor:
    def __init__(self, name="Sensor", type="SONIC", memsize=10, pin=[], outf=None, inf=None):
        self.name = name
        self.type = type
        self.pin = pin
        self.queue = queue.Queue(memsize)
        self.state = False
        self.outf = outf
        self.inf = inf
        self.meta = dict()
        self.out = None
        self.inp = None
        self.bad = False
        self.lock = threading.RLock()

    def on(self):
        if self.state:
            return
        self.state = True
        if not self.out:
            self.out = threading.Thread(target=self.output)
            self.out.start()
        if not self.inp:
            self.inp = threading.Thread(target=self.input)
            self.inp.start()

    def off(self):
        if not self.state:
            return
        self.state = False
        self.out.join()
        self.inp.join()
        self.out = None
        self.inp = None

    def output(self):
        if not self.state:
            return
        while self.state:
            self.lock.acquire()
            out = self.outf()
            self.lock.release()
            self.queue.put(out)
            self.queue.task_done()

    def input(self):
        if not self.state:
            return
        if (self.queue.empty()):
            return None
        return self.queue.get(block=False, timeout=None)

    def reset(self):
        while not self.queue.empty():
            self.queue.get(block=False, timeout=None)
