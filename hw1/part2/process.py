import os
import time


class Process:
    def __init__(self):
        self.pid = os.getpid()
        self.zombies = []
        self.orphans = []

    def __str__(self):
        return f"Process {self.pid} with {len(self.zombies)} zombies and {len(self.orphans)} orphans" \
               f" (zombies: {self.zombies}, orphans: {self.orphans})"

    def generate_zombie(self):
        zombie = Zombie()
        self.zombies.append(zombie)
        return zombie

    def generate_orphan(self):
        orphan = Orphan()
        self.orphans.append(orphan)
        return orphan

    def cleanup_zombies(self):
        self.zombies = [z for z in self.zombies if not z.is_zombie()]

    def __del__(self):
        self.cleanup_zombies()


class Orphan:
    def __init__(self):
        self.pid = os.fork()
        if self.pid == 0:  # Child process
            print(f"Orphan {os.getpid()} is created.")
            time.sleep(5)  # Sleep for 5 seconds to keep the orphan alive.

    def is_zombie(self):
        try:
            # Sending signal 0 to check if the process exists.
            os.kill(self.pid, 0)
            return False
        except ProcessLookupError:
            return True


class Zombie:
    def __init__(self):
        self.pid = os.fork()
        if self.pid == 0:  # Child process
            print(f"Zombie {os.getpid()} is created.")
            time.sleep(5)  # Sleep for 5 seconds to make it a zombie.

    def is_zombie(self):
        try:
            # Sending signal 0 to check if the process exists.
            os.kill(self.pid, 0)
            return False
        except ProcessLookupError:
            return True

# if __name__ == "__main__":
#     parent = Process()
#
#     time.sleep(10)  # Sleep for 10 seconds to keep the orphans alive.
#
#     print(f"Parent process {os.getpid()} terminated.")
