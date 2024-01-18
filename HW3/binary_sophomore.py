import threading
import time


class BinarySemaphore:
    def __init__(self, initial_value=1):
        self.value = initial_value
        self.lock = threading.Lock()
        self.condition = threading.Condition(lock=self.lock)
        self.current_holder = None

    def acquire(self, process_id):
        with self.lock:
            while self.value == 0:
                print(f"Process {process_id} waiting to enter critical section.")
                self.condition.wait()
            self.value = 0
            self.current_holder = process_id

    def release(self):
        with self.lock:
            self.value = 1
            self.current_holder = None
            self.condition.notify()


class SharedResource:
    def __init__(self, initial_value=0, binary_semaphore=None):
        self.value = initial_value
        self.lock = threading.Lock()
        self.binary_semaphore = binary_semaphore

    def modify(self, process_id):
        with self.lock:
            if self.value == 0 and self.binary_semaphore.current_holder != process_id:
                print(f"Warning: Process {process_id} trying to interfere with another process in critical section.")
            else:
                self.value += 1
                print(f"Process {process_id} modified shared resource: {self.value}")


class Process(threading.Thread):
    def __init__(self, process_id, binary_semaphore, shared_resource):
        super(Process, self).__init__()
        self.process_id = process_id
        self.binary_semaphore = binary_semaphore
        self.shared_resource = shared_resource

    def run(self):
        self.binary_semaphore.acquire(self.process_id)

        self.shared_resource.modify(self.process_id)

        self.binary_semaphore.release()


def main():
    n = int(input("Enter the number of processes: "))

    binary_semaphore = BinarySemaphore()
    shared_resource = SharedResource(binary_semaphore=binary_semaphore)

    processes = [Process(i, binary_semaphore, shared_resource) for i in range(n)]

    for process_thread in processes:
        process_thread.start()

    time.sleep(1)

    for process_thread in processes:
        process_thread.join()
