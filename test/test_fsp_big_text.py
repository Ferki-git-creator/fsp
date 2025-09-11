import time
from collections import defaultdict
import struct

def find_patterns(text, min_len=3, max_len=5):
    patterns = defaultdict(list)
    n = len(text)
    for L in range(min_len, max_len + 1):
        for i in range(n - L + 1):
            s = text[i:i+L]
            patterns[s].append(i)
    # Keep only patterns that occur more than once
    return {p: pos for p, pos in patterns.items() if len(pos) > 1}

def fsp_compress(text, min_len=3, max_len=5):
    patterns = find_patterns(text, min_len, max_len)
    compressed = bytearray()
    i = 0
    while i < len(text):
        best_pat = None
        best_pos = None
        best_len = 0
        for pat, positions in patterns.items():
            if i in positions and len(pat) > best_len:
                prev_positions = [p for p in positions if p < i]
                if prev_positions:
                    best_pat = pat
                    best_pos = prev_positions[-1]
                    best_len = len(pat)
        if best_pat and best_pos is not None:
            # REF: 2 bytes pos + 1 byte len
            compressed += struct.pack(">HB", best_pos, best_len)
            i += best_len
        else:
            # LITERAL: 1 byte
            compressed.append(ord(text[i]))
            i += 1
    return compressed

def fsp_decompress(compressed):
    output = []
    i = 0
    while i < len(compressed):
        # Check if next 3 bytes could be a REF
        if i + 3 <= len(compressed):
            pos, length = struct.unpack(">HB", compressed[i:i+3])
            # Valid REF: pos < len(output)
            if pos < len(output):
                output.extend(output[pos:pos+length])
                i += 3
                continue
        # Otherwise, literal
        output.append(compressed[i])
        i += 1
    return bytes(output).decode("ascii")

# -----------------------
# Test compression
# -----------------------
if __name__ == "__main__":
    text = """Two households, both alike in dignity,
In fair Verona, where we lay our scene,
From ancient grudge break to new mutiny,
Where civil blood makes civil hands unclean.
From forth the fatal loins of these two foes
A pair of star-crossed lovers take their life;
Whose misadventured piteous overthrows
Doth with their death bury their parents' strife.
The fearful passage of their death-marked love,
And the continuance of their parents' rage,"""

    original_size = len(text.encode("ascii"))

    # Compression timing
    start_time = time.time()
    compressed = fsp_compress(text)
    compress_time = time.time() - start_time

    compressed_size = len(compressed)

    # Save compressed to file
    with open("output.txt", "wb") as f:
        f.write(compressed)

    # Decompression timing
    start_time = time.time()
    decompressed = fsp_decompress(compressed)
    decompress_time = time.time() - start_time

    assert decompressed == text, "Decompressed data does not match original!"

    ratio = original_size / compressed_size if compressed_size > 0 else 0
    print("Original size:", original_size, "bytes")
    print("Compressed size:", compressed_size, "bytes")
    print("Compression ratio:", round(ratio, 2))
    print(f"Compression time: {compress_time:.4f} sec")
    print(f"Decompression time: {decompress_time:.4f} sec")