from notify_run import Notify

def push(msg=""):
    notify = Notify()
    warning = 'KBot Breach'
    if msg:
        warning = msg
    notify.send(warning, 'http://th3ri5k.mynetgear.com/kbot/logs.html')