from sensor import sensor
import RPi.GPIO as GPIO
import time

class ultrasonic:
    def __init__(self, name="ULTRASONIC", memsize=10, ultrasonicPin=12):
        self.sonic = sensor(name, "ULTRASONIC", 1, ultrasonicPin, self.ping)
        self.state = False
        self.pin = None

    def on(self):
        self.sonic.on()
        #self.sweep.on()
        self.state = True

    def off(self):
        self.sonic.off()
        #self.sweep.off()
        self.state = False

    # def sweep(self, deg=1, rate=0.005, srange=[10.0, 180.0]):
    #     if not self.state: return
    #     sweep = list(range(int(srange[0]), int(srange[1]), deg))
    #     sweep += list(reversed(sweep))
    #     for i in sweep:
    #         self.sweep.pin.rotate(i)
    #         self.sweep.meta['angle'] = i
    #         time.sleep(rate)

    def ping(self):
        if not self.state: return None

        pin = self.sonic.pin.pin_id

        starttime = time.time()
        endtime = time.time()
        distance = -1

        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
        time.sleep(0.000002)
        GPIO.output(pin, 1)
        time.sleep(0.000005)
        GPIO.output(pin, 0)
        GPIO.setup(pin, GPIO.IN)
        while GPIO.input(pin) == 0:
            starttime=time.time()
        while GPIO.input(pin) == 1:
            endtime=time.time()
        duration=endtime-starttime
        # Distance is defined as time/2 (there and back) * speed of sound 34300 cm/s
        distance = (duration*34300.0)/2.0

        print("distance: " + str(distance))

        return starttime, distance

    def reset(self):
        self.sonic.reset()

    def input(self):
        return self.sonic.input()
