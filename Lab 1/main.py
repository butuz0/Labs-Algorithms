import time
from file_manager import Sort, AdvancedSort

size = 10
files_amount = 16
chunk_amount = 16*8

# file = Sort("file.bin", size, files_amount)
# file.create_file()
# start = time.time()
# file.sort()
# print(f"sorting time of {size}mb: ", time.time()-start)

file = AdvancedSort("file.bin", size, files_amount, chunk_amount)
file.create_file()
start = time.time()
file.advanced_sort()
print(f"sorting time of {size}mb: ", time.time()-start)
