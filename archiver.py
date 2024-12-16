import os

def bwt_encode(text):
    """Perform Burrows-Wheeler Transform encoding."""
    if not text:
        return "", 0
        
    # Add EOF character
    text += '\0'
    
    # Create rotations
    rotations = []
    for i in range(len(text)):
        rotation = text[i:] + text[:i]
        rotations.append(rotation)
    
    # Sort rotations
    rotations.sort()
    
    # Find original string index
    original_idx = rotations.index(text)
    
    # Get last column
    last_column = ''.join(rotation[-1] for rotation in rotations)
    
    return last_column, original_idx

def bwt_decode(last_column, original_idx):
    """Perform Burrows-Wheeler Transform decoding."""
    if not last_column:
        return ""
        
    # Create first column by sorting last column
    first_column = ''.join(sorted(last_column))
    
    # Create transformation table
    table = []
    for i in range(len(last_column)):
        table.append([first_column[i], last_column[i]])
    
    # Sort table by last column when first columns are equal
    for _ in range(len(last_column) - 1):
        table.sort()
        for i in range(len(last_column)):
            table[i].insert(0, last_column[i])
    
    # Get original text from the row indicated by original_idx
    row = table[original_idx]
    text = ''.join(row)
    
    # Remove EOF character
    if '\0' in text:
        text = text[:text.index('\0')]
    
    return text

def rle_encode(text):
    """Perform Run-Length Encoding."""
    if not text:
        return ""
        
    encoded = []
    count = 1
    current = text[0]
    
    for char in text[1:]:
        if char == current:
            count += 1
        else:
            encoded.append(f"{count}{current}")
            current = char
            count = 1
            
    encoded.append(f"{count}{current}")
    return ''.join(encoded)

def rle_decode(text):
    """Perform Run-Length Decoding."""
    if not text:
        return ""
        
    decoded = []
    count = ""
    
    for char in text:
        if char.isdigit():
            count += char
        else:
            decoded.append(char * int(count))
            count = ""
            
    return ''.join(decoded)

def compress_file(input_path, output_path):
    """Compress file using BWT+RLE."""
    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Apply BWT
        bwt_text, original_idx = bwt_encode(text)
        
        # Apply RLE
        compressed = rle_encode(bwt_text)
        
        # Write compressed data
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"{original_idx}\n")  # First line is the original index
            f.write(compressed)  # Rest is the compressed data
            
        # Calculate compression ratio
        input_size = os.path.getsize(input_path)
        output_size = os.path.getsize(output_path)
        compression_ratio = (1 - output_size/input_size) * 100
        
        print(f"Compression complete!")
        print(f"Original size: {input_size} bytes")
        print(f"Compressed size: {output_size} bytes")
        print(f"Compression ratio (SSR): {compression_ratio:.2f}%")
        
    except Exception as e:
        print(f"Error during compression: {e}")

def decompress_file(input_path, output_path):
    """Decompress file using BWT+RLE."""
    try:
        # Read compressed file
        with open(input_path, 'r', encoding='utf-8') as f:
            original_idx = int(f.readline())  # First line is the original index
            compressed = f.read()  # Rest is the compressed data
        
        # Apply RLE decode
        bwt_text = rle_decode(compressed)
        
        # Apply BWT decode
        decompressed = bwt_decode(bwt_text, original_idx)
        
        # Write decompressed data
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(decompressed)
            
        print("Decompression complete!")
        
    except Exception as e:
        print(f"Error during decompression: {e}")

def compare_files(file1, file2):
    """Compare two files and print differences."""
    try:
        with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
            text1 = f1.read()
            text2 = f2.read()
            
        if text1 == text2:
            print("Files are identical!")
        else:
            print("Files are different!")
            # You could implement more detailed diff here
            
    except Exception as e:
        print(f"Error comparing files: {e}")

def main():
    input_file = "Felis_catus.Felis_catus_9.0.dna.chromosome.A1.fa"
    compressed_file = "compressed.bin"
    decompressed_file = "decompressed.fa"
    
    # Compress
    print("Compressing file...")
    compress_file(input_file, compressed_file)
    
    # Decompress
    print("\nDecompressing file...")
    decompress_file(compressed_file, decompressed_file)
    
    # Compare
    print("\nComparing original and decompressed files...")
    compare_files(input_file, decompressed_file)

if __name__ == "__main__":
    main()
