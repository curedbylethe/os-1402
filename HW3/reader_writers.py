import threading
import time
import random


class ReadersWritersSimulation:
    def __init__(self):
        self.shared_resource = 0
        self.readers_count = 0
        self.resource_lock = threading.Lock()
        self.readers_semaphore = threading.Semaphore()
        self.writers_semaphore = threading.Semaphore()

    def read(self, reader_id):
        with self.readers_semaphore:
            with self.resource_lock:
                self.readers_count += 1
                if self.readers_count == 1:
                    self.writers_semaphore.acquire()

        print(f"Reader {reader_id} is reading. Shared Resource Value: {self.shared_resource}")
        time.sleep(random.uniform(0.1, 0.5))

        with self.readers_semaphore:
            with self.resource_lock:
                self.readers_count -= 1
                if self.readers_count == 0:
                    self.writers_semaphore.release()

    def write(self, writer_id):
        with self.writers_semaphore:
            with self.resource_lock:
                self.shared_resource += 1
                print(f"Writer {writer_id} is writing. Shared Resource Value: {self.shared_resource}")
                time.sleep(random.uniform(0.1, 0.5))


def simulate_readers_writers(simulation, num_readers, num_writers):
    readers = [threading.Thread(target=simulation.read, args=(i,)) for i in range(num_readers)]
    writers = [threading.Thread(target=simulation.write, args=(i,)) for i in range(num_writers)]

    all_threads = readers + writers
    random.shuffle(all_threads)

    for thread in all_threads:
        thread.start()

    for thread in all_threads:
        thread.join()


def main():
    simulation = ReadersWritersSimulation()
    num_readers = int(input("Enter the number of readers: "))
    num_writers = int(input("Enter the number of writers: "))

    simulate_readers_writers(simulation, num_readers, num_writers)
