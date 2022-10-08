import random
import os
import time


class File:
    def __init__(self, path):
        self.path = path
        self.file = open(path, "rb")
        self.prev = (0).to_bytes(32, byteorder="big")
        self.curr = self.file.read(32)
        self.next = self.file.read(32)

    def __next__(self):
        self.prev = self.curr
        self.curr = self.next
        self.next = self.file.read(32)


class Writer:
    def __init__(self, path):
        self.path = path
        self.file = open(path, "ab")


class Sort:
    def __init__(self, path, size_mb, files_amount):
        self.path = path
        self.size = int(size_mb * (1024 ** 2) / 32)
        self.files_amount = files_amount

    def create_file(self):
        print("creating random file...")
        with open(self.path, "wb") as file:
            for i in range(self.size):
                file.write(random.randint(1, 10_000).to_bytes(32, byteorder="big"))

    @staticmethod
    def all_files_read(files):
        return sum([int.from_bytes(file.curr, byteorder="big") for file in files]) == 0

    @staticmethod
    def clear_file(path):
        open(path, 'w').close()

    @staticmethod
    def get_file_list(path):
        file = open(path, "rb")
        arr = []
        elem = int.from_bytes(file.read(32), byteorder="big")
        while elem != 0:
            arr.append(elem)
            elem = int.from_bytes(file.read(32), byteorder="big")
        return arr

    @staticmethod
    def get_file_size(path):
        return os.stat(path).st_size

    def find_series(self):
        print("\nfinding series...")
        start = time.time()

        files = []
        for i in range(self.files_amount):
            x = Writer(f"B{i + 1}.bin")
            files.append(x)

        a = File(self.path)
        series = [a.curr]
        file_number = 0
        for i in range(self.size):
            if a.next >= a.curr:
                series.append(a.next)
            else:
                for elem in series:
                    files[file_number].file.write(elem)

                file_number += 1
                if file_number == self.files_amount:
                    file_number = 0

                series = [a.next]
            next(a)
        print("finding series time: ", time.time() - start)

    def merge(self, file_name1, file_name2):
        print("\nmerging...")
        start = time.time()

        merge_files = []
        for i in range(self.files_amount):
            self.clear_file(f"{file_name2}{i + 1}.bin")
            x = Writer(f"{file_name2}{i + 1}.bin")
            merge_files.append(x)

        distribute_files = []
        for i in range(self.files_amount):
            file = File(f"{file_name1}{i + 1}.bin")
            distribute_files.append(file)

        files_read = False
        while not files_read:
            for m_file in merge_files:
                if self.all_files_read(distribute_files):
                    files_read = True
                    break

                for file in distribute_files:
                    file.prev = (0).to_bytes(32, byteorder="big")

                while True:
                    min_elem_file = -1
                    min_elem = (10001).to_bytes(32, byteorder="big")

                    for i in range(len(distribute_files)):
                        if distribute_files[i].prev <= distribute_files[i].curr <= min_elem:
                            min_elem = distribute_files[i].curr
                            min_elem_file = i

                    if min_elem == (10001).to_bytes(32, byteorder="big"):
                        break

                    m_file.file.write(min_elem)
                    next(distribute_files[min_elem_file])
        print("merging time: ", time.time() - start)

    def sort(self):
        for i in range(self.files_amount):
            self.clear_file(f"B{i + 1}.bin")
            self.clear_file(f"C{i + 1}.bin")
        files = ["B", "C"]
        self.find_series()
        while self.get_file_size("file.bin") != self.get_file_size("B1.bin") and self.get_file_size("file.bin") != self.get_file_size("C1.bin"):
            self.merge(files[0], files[1])
            files[0], files[1] = files[1], files[0]


class AdvancedSort(Sort):
    def __init__(self, path, size_mb, files_amount, chunks_amount):
        super().__init__(path, size_mb, files_amount)
        self.chunk_amount = chunks_amount

    def advanced_distribution(self):
        print("\ndistributing...")
        start = time.time()
        a = File(self.path)
        files = []
        for i in range(self.files_amount):
            self.clear_file(f"B{i + 1}.bin")
            x = Writer(f"B{i + 1}.bin")
            files.append(x)

        for i in range(self.chunk_amount):
            series = []
            while a.curr != 0 and len(series) < self.size/self.chunk_amount:
                series.append(a.curr)
                next(a)
            series.sort()
            for elem in series:
                files[i % self.files_amount].file.write(elem)
        print("distributing time: ", time.time() - start)

    def advanced_merge1(self):
        print("\nmerging...")
        start = time.time()

        merge_files = []
        for i in range(int(self.chunk_amount/self.files_amount)):
            self.clear_file(f"C{i + 1}.bin")
            x = Writer(f"C{i + 1}.bin")
            merge_files.append(x)

        distribute_files = []
        for i in range(self.files_amount):
            file = File(f"B{i + 1}.bin")
            distribute_files.append(file)

        for j in range(int(self.chunk_amount/self.files_amount)):

            for file in distribute_files:
                file.prev = (0).to_bytes(32, byteorder="big")

            while True:
                min_elem_file = -1
                min_elem = (10001).to_bytes(32, byteorder="big")

                for i in range(len(distribute_files)):
                    if distribute_files[i].prev <= distribute_files[i].curr <= min_elem:
                        min_elem = distribute_files[i].curr
                        min_elem_file = i

                if min_elem == (10001).to_bytes(32, byteorder="big"):
                    break

                merge_files[j].file.write(min_elem)
                next(distribute_files[min_elem_file])
        print("merging time: ", time.time()-start)

    def advanced_merge2(self):
        print("\nmerging...")
        start = time.time()
        for i in range(self.files_amount):
            self.clear_file(f"B{i+1}.bin")
        b_file = Writer("B1.bin")

        distribute_files = []
        for i in range(int(self.chunk_amount/self.files_amount)):
            file = File(f"C{i + 1}.bin")
            distribute_files.append(file)

        while True:
            min_elem_file = -1
            min_elem = (10001).to_bytes(32, byteorder="big")

            for i in range(len(distribute_files)):
                if distribute_files[i].prev <= distribute_files[i].curr <= min_elem:
                    min_elem = distribute_files[i].curr
                    min_elem_file = i

            if min_elem == (10001).to_bytes(32, byteorder="big"):
                break

            b_file.file.write(min_elem)
            next(distribute_files[min_elem_file])
        print("merging time: ", time.time() - start)

    def advanced_sort(self):
        for i in range(self.files_amount):
            self.clear_file(f"B{i + 1}.bin")
            self.clear_file(f"C{i + 1}.bin")
        self.advanced_distribution()
        self.advanced_merge1()
        self.advanced_merge2()
