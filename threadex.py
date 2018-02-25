import threading
import time
import schedule

class Threading(object):

    def __init__(self, interval=60):

        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            schedule.run_pending()
            time.sleep(self.interval)