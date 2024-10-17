import random
import time
import threading
from collections import deque


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

    def is_free(self):
        return self.guest is None

    def sit_guest(self, guest):
        self.guest = guest

    def leave_table(self):
        self.guest = None


class Queue:
    def __init__(self):
        self.queue = deque()

    def add_guest(self, guest):
        self.queue.append(guest)

    def get_next_guest(self):
        return self.queue.popleft() if self.queue else None

    def empty(self):
        return len(self.queue) == 0


class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        wait_time = random.randint(3, 10)
        print(f"{self.name} ожидает {wait_time} секунд...")
        time.sleep(wait_time)


class Cafe:
    def __init__(self, *tables):
        self.tables = tables
        self.queue = Queue()

    def guest_arrival(self, *guests):
        for guest in guests:
            table = self.find_free_table()
            if table:
                table.sit_guest(guest)
                print(f"{guest.name} сел(-а) за стол номер {table.number}")
                guest.start()
            else:
                self.queue.add_guest(guest)
                print(f"{guest.name} в очереди")

    def find_free_table(self):
        for table in self.tables:
            if table.is_free():
                return table
        return None

    def discuss_guests(self):
        while not self.queue.empty() or any(not table.is_free() for table in self.tables):
            for table in self.tables:
                if not table.is_free():
                    guest = table.guest
                    if not guest.is_alive():
                        print(f"{guest.name} покушал(-а) и ушёл(ушла)")
                        print(f"Стол номер {table.number} свободен")
                        table.leave_table()


                        next_guest = self.queue.get_next_guest()
                        if next_guest:
                            table.sit_guest(next_guest)
                            print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                            next_guest.start()
            time.sleep(1)


# Пример использования
if __name__ == "__main__":
    cafe = Cafe(Table(1), Table(2), Table(3))

    guest1 = Guest("Вася")
    guest2 = Guest("Маша")
    guest3 = Guest("Петя")
    guest4 = Guest("Анна")

    cafe.guest_arrival(guest1, guest2, guest3, guest4)

    time.sleep(5)
    cafe.discuss_guests()
