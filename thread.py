import threading

class AudioThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(AudioThread, self).__init__(*args, **kwargs)
        self.killed = False
        self.setDaemon(True)

    def kill(self):
        self.killed = True
