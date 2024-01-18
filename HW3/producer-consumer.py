import threading
import time
import random


class SharedBuffer:
    def __init__(self, max_size, total_items):
        self.buffer = []
        self.max_size = max_size
        self.buffer_lock = threading.Lock()
        self.items_produced = 0
        self.items_consumed = 0
        self.total_items = total_items

    def produce(self, producer_id):
        item = random.randint(1, 100)
        with self.buffer_lock:
            while len(self.buffer) == self.max_size and self.items_produced < self.total_items:
                print(f"Buffer is full. Producer {producer_id} is waiting...")
                self.buffer_lock.release()
                time.sleep(random.uniform(0.1, 0.5))
                self.buffer_lock.acquire()

            if self.items_produced < self.total_items:
                self.buffer.append(item)
                self.items_produced += 1
                print(f"Producer {producer_id}, produced {item}. Total items have been produced: {self.items_produced}")

    def consume(self, consumer_id):
        with self.buffer_lock:
            while len(self.buffer) == 0 and self.items_consumed < self.total_items:
                self.buffer_lock.release()
                time.sleep(random.uniform(0.1, 0.5))
                self.buffer_lock.acquire()

            if self.items_consumed < self.total_items:
                item = self.buffer.pop(0)
                self.items_consumed += 1
                print(f"Consumer {consumer_id}, consumed {item}. Total items have been consumed: {self.items_consumed}")


def producer_function(producer_id, shared_buffer):
    while shared_buffer.items_produced < shared_buffer.total_items:
        shared_buffer.produce(producer_id)


def consumer_function(consumer_id, shared_buffer):
    while shared_buffer.items_consumed < shared_buffer.total_items:
        shared_buffer.consume(consumer_id)


def main():
    buffer_size = 5
    total_items = 500
    num_producers = 5
    num_consumers = 3

    shared_buffer = SharedBuffer(max_size=buffer_size, total_items=total_items)

    producer_threads = [threading.Thread(target=producer_function, args=(i, shared_buffer)) for i in
                        range(num_producers)]
    consumer_threads = [threading.Thread(target=consumer_function, args=(i, shared_buffer)) for i in
                        range(num_consumers)]

    all_threads = producer_threads + consumer_threads
    random.shuffle(all_threads)

    for thread in all_threads:
        thread.start()

    for thread in all_threads:
        thread.join()


if __name__ == "__main__":
    main()
