from utils import *

from pymesos import MesosSchedulerDriver
from custom_scheduler import CustomScheduler
from threading import Thread
import signal
import time
import sys


def startup(master):
    executor = new_executor(10, .1)
    framework = build_framework()

    driver = MesosSchedulerDriver(
        CustomScheduler(executor),
        framework,
        master,
        use_addict=True,
    )

    def signal_handler(signal, frame):
        driver.stop()

    def run_driver_thread():
        driver.run()

    driver_thread = Thread(target=run_driver_thread, args=())
    driver_thread.start()

    print('Scheduler running, Ctrl+C to quit.')
    signal.signal(signal.SIGINT, signal_handler)

    while driver_thread.is_alive():
        time.sleep(1)


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) != 2:
        print("Using default mesos master (zk://0.0.0.0:2181/mesos)".format(sys.argv[0]))
        master = "0.0.0.0:5050"
    else:
        master = sys.argv[1]

    startup(master)
