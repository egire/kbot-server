from notify_run import Notify

def push(msg=""):
    notify = Notify()
    warning = 'KBot Breach'
    if msg:
        warning = msg
    notify.send(warning, 'http://moonman1.mynetgear.com/kbot/logs.html')