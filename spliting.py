import os
import time

start = time.time()

os.system(
    """spleeter separate -p spleeter:2stems input/chuyenrang.mp3 -o output -c wav""")

print(time.time() - start)
