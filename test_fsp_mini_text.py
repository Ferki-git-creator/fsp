# ---------------------------
# Next Level FSP Test: Short Text
# ---------------------------

def find_patterns(text, min_len=3, max_len=5):
    """Find repeated substrings of length min_len to max_len in text"""
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
            # add substrings of length min_len..max_len starting at i
            for l2 in range(min_len, max_len + 1):
                if i + l2 <= len(text):
                    refs[text[i:i + l2]] = i
            i += 1
    return compressed

def decompress_fsp(compressed):
    result = []
    i = 0
    text = ""
    for item in compressed:
        if item[0] == "LITERAL":
            text += item[1]
        elif item[0] == "REF":
            pos, length = item[1], item[2]
            text += text[pos:pos + length]
    return text

# ---------------------------
# Test with short text
# ---------------------------

data = "Hello friend! Hello fiend! Hello friends! Hello friend!"
original_size = len(data.encode('utf-8'))

compressed = find_patterns(data)
compressed_size = 0
for tag, *content in compressed:
    if tag == "LITERAL":
        compressed_size += 1  # 1 byte per char
    elif tag == "REF":
        compressed_size += 2  # 1 byte pos + 1 byte length (approx)

ratio = original_size / compressed_size if compressed_size > 0 else 0
restored = decompress_fsp(compressed)
assert restored == data, "Decompressed text does not match original!"

print("Original size:", original_size, "bytes")
print("Estimated compressed size:", compressed_size, "bytes")
print("Compression ratio:", round(ratio, 2))
print("\nCompressed representation:")
for item in compressed:
    print(item)