import os

def generate_dataset(size):
    
    with open("/dev/urandom", "rb") as f:
        raw = f.read(size * 4)  # 
    nums = [int.from_bytes(raw[i:i+4], "little") for i in range(0, len(raw), 4)]
    return nums[:size]