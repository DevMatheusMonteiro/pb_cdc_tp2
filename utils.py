import time

def print_timestamp(msg: str):
    print(f"[{time.strftime("%H:%M:%S")}] {msg}")
