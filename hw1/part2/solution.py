# from a parent process, generate a zombie and an orphan, and then guide the orphan to terminate.
import time

from .process import Process


def main():
    # generate a zombie and an orphan
    process = Process()

    for _ in range(2):
        process.generate_zombie()
    for _ in range(2):
        process.generate_orphan()

    time.sleep(10)

    # print the process
    print(process)
