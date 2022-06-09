import os
import time

start = time.time()

os.system(
    """spleeter separate -p spleeter:2stems input/nangtho.mp3 -o output -c mp3""")

print(time.time() - start)
