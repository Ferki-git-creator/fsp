from collections import defaultdict

def find_patterns(text, min_len=3, max_len=5):
    """Find repeated patterns in text and return dictionary with positions"""
    patterns = defaultdict(list)
    n = len(text)
    for L in range(min_len, max_len + 1):
        for i in range(n - L + 1):
            s = text[i:i+L]
            patterns[s].append(i)
    # Keep only patterns that occur more than once
    return {p: pos for p, pos in patterns.items() if len(pos) > 1}

def next_level_fsp_compress(text, min_len=3, max_len=5):
    patterns = find_patterns(text, min_len, max_len)
    compressed = []
    used = [False] * len(text)
    
    i = 0
    while i < len(text):
        # Try to find the longest pattern starting at i
        best_pat = None
        best_pos = None
        best_len = 0
        for pat, positions in patterns.items():
            if i in positions and len(pat) > best_len:
                # Find first previous occurrence
                prev_positions = [p for p in positions if p < i]
                if prev_positions:
                    best_pat = pat
                    best_pos = prev_positions[-1]
                    best_len = len(pat)
        if best_pat and best_pos is not None:
            compressed.append(("REF", best_pos, best_len))
            for j in range(best_len):
                used[i+j] = True
            i += best_len
        else:
            compressed.append(("LITERAL", text[i]))
            i += 1
    return compressed

def next_level_fsp_decompress(compressed):
    """Corrected decompression using a running text buffer"""
    output_str = ""
    for item in compressed:
        if item[0] == "LITERAL":
            output_str += item[1]
        elif item[0] == "REF":
            pos, length = item[1], item[2]
            ref_text = output_str[pos:pos+length]
            output_str += ref_text
    return output_str

# -----------------------
# Test next-level FSP
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

    original_size = len(text.encode("utf-8"))
    compressed = next_level_fsp_compress(text)
    
    # Rough estimate of compressed size
    compressed_size = 0
    for tag, *data in compressed:
        if tag == "LITERAL":
            compressed_size += 1
        elif tag == "REF":
            compressed_size += 2  # rough estimate: position + length

    decompressed = next_level_fsp_decompress(compressed)
    assert decompressed == text, "Decompressed data does not match original!"
    
    ratio = original_size / compressed_size if compressed_size > 0 else 0
    print("Original size:", original_size, "bytes")
    print("Estimated compressed size:", compressed_size, "bytes")
    print("Compression ratio:", round(ratio, 2))
    print("\nCompressed representation:")
    for item in compressed:
        print(item)