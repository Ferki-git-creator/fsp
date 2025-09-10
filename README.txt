FSP — Find Similar Patterns (Next Level Update)    

ALGORITHM DESCRIPTION    

FSP is a universal data compression algorithm for any files or byte streams. Its core idea is to find similar patterns in data and store only the differences or references, avoiding duplication. This next-level update adds automatic pattern length selection, optimized reference handling, and extended max pattern lengths for long repeats.  

AUTOMATIC MINIMUM PATTERN SELECTION    

- The algorithm scans the text/data and automatically selects a minimum pattern length between 3–5 characters.  
- The chosen length maximizes repeated patterns while avoiding overhead from too-short sequences.  

MINIMIZED REF OVERHEAD    

- Patterns that repeat only once are stored as LITERAL instead of creating a REF.  
- This avoids unnecessary reference overhead and keeps compressed data compact.  

MAXIMUM PATTERN LENGTH SELECTION    

- For longer repeated blocks, the algorithm searches for patterns up to 5–6 characters long.  
- Longer patterns improve compression for large repeated sequences without increasing complexity.  

SIMPLE EXPLANATION    

Think of a LEGO box analogy:  

1. Pick one construction as the base.  
2. Store similar constructions as base + differences only.  
3. Unique constructions remain unchanged.  
4. You save space by storing only new details instead of the entire construction.  

EXAMPLE    

Text:  
Base: "Hello friend!"  
Similar: "Hello fiend!"  
Store:  
- Base as LITERAL  
- Differences: position 7 -> "i"  
During decompression: apply differences to base → get original similar line.  

BYTE DATA EXAMPLE    

- Works for any byte file or stream.  
- Split data into blocks or patterns.  
- Store one base block/pattern.  
- Store repeated blocks as references or differences.  
- Unique blocks store fully.  

NEW USE CASES    

- Logs and journals with almost repeating lines  
- File versions and incremental backups  
- Sets of images with minor differences  
- Video frames with slight changes  
- Any data where repeated patterns exist  
- Text or byte streams where 3–5 character pattern matching is sufficient  

IMPLEMENTATION STEPS    

1. Scan entire data to find repeated patterns of length 3–5 automatically.  
2. Create a list of base patterns.  
3. For each new pattern:  
   a. Check for a similar pattern in base patterns.  
   b. If similar, store as REF (offset + length) or differences.  
   c. If unique, store as LITERAL.  
4. Record results:  
   - Base patterns  
   - References/differences for repeated patterns  
   - Unique LITERAL data  
5. Decompression:  
   a. Load base patterns  
   b. Apply references/differences to reconstruct repeated patterns  
   c. Add unique LITERAL data unchanged  

PATTERN LENGTH GUIDELINES    

- Automatic min_len = 3–5 characters  
- Max pattern length = 5–6 characters for longer repeats  
- Optimal min/max values adapt to data type:  
   * Short repetitive text → min_len=3, max_len=5  
   * Longer logs/technical text → min_len=4, max_len=6  

FEATURES    

- Automatic pattern length selection for maximum compression  
- Minimized REF overhead to prevent size inflation  
- Handles long repeated patterns efficiently  
- Simple LITERAL + REF format  
- Works on any type of data stream  
- No complex data structures needed  
- Cross-language implementable (Python, C, C++, Java, Rust, Go, etc.)  

SUMMARY    

Next-level FSP is simple, universal, and powerful. It automatically adapts pattern lengths, minimizes unnecessary references, and effectively compresses data with repeated sequences. Ideal for text, byte streams, backups, logs, images, or any data with repeated patterns, providing significant file size reduction without data loss.  

LICENSE    

Licensed under LGPL 3.0.