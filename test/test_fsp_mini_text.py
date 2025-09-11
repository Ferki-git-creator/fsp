import time

# ---------------------------
# Next Level FSP Compression
# ---------------------------

def find_patterns(text, min_len=3, max_len=5):
    """Find repeated substrings and compress text"""
    refs = {}
    i = 0
    compressed = []
    while i < len(text):
        match_len = 0
        match_pos = 0
        # search for longest match in refs
        for l in range(max_len, min_len - 1, -1):
            if i + l <= len(text):
                s = text[i:i + l]
                if s in refs:
                    match_len = l
                    match_pos = refs[s]
                    break
        if match_len > 0:
            compressed.append(("REF", match_pos, match_len))
            # add new substrings in this range to refs
            for l2 in range(min_len, match_len + 1):
                for j in range(i, i + match_len - l2 + 1):
                    refs[text[j:j + l2]] = j
            i += match_len
        else:
            compressed.append(("LITERAL", text[i]))
            for l2 in range(min_len, max_len + 1):
                if i + l2 <= len(text):
                    refs[text[i:i + l2]] = i
            i += 1
    return compressed

def decompress_fsp(compressed):
    text = ""
    for item in compressed:
        if item[0] == "LITERAL":
            text += item[1]
        elif item[0] == "REF":
            pos, length = item[1], item[2]
            text += text[pos:pos + length]
    return text

def save_compressed(compressed, filename="output.txt"):
    """Save compressed data byte-by-byte"""
    with open(filename, "wb") as f:
        for item in compressed:
            if item[0] == "LITERAL":
                f.write(b'\x00')          # marker for LITERAL
                f.write(item[1].encode('utf-8'))
            elif item[0] == "REF":
                f.write(b'\x01')          # marker for REF
                f.write(bytes([item[1]])) # position (1 byte, works for small test)
                f.write(bytes([item[2]])) # length (1 byte)

# ---------------------------
# Test with short text
# ---------------------------

data = "Hello friend! Hello fiend! Hello friends! Hello friend!"
original_size = len(data.encode('utf-8'))

start_comp = time.time()
compressed = find_patterns(data)
end_comp = time.time()

start_decomp = time.time()
restored = decompress_fsp(compressed)
end_decomp = time.time()

assert restored == data, "Decompressed text does not match original!"

# accurate counting
compressed_size = 0
for item in compressed:
    if item[0] == "LITERAL":
        compressed_size += 1
    elif item[0] == "REF":
        compressed_size += 2  # pos + length

ratio = original_size / compressed_size if compressed_size > 0 else 0

print("Original size:", original_size, "bytes")
print("Compressed size:", compressed_size, "bytes")
print("Compression ratio:", round(ratio, 2))
print("Compression time:", round(end_comp - start_comp, 6), "sec")
print("Decompression time:", round(end_decomp - start_decomp, 6), "sec")
print("\nCompressed representation:")
for item in compressed:
    print(item)

# Save compressed to file
save_compressed(compressed)