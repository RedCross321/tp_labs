import os
from typing import Tuple, List

def bwt_encode(text: str) -> Tuple[str, int]:
    """
    Выполняет прямое преобразование Барроуза-Уилера.
    Возвращает преобразованный текст и индекс исходной строки.
    """
        
    text = text + '$'
    
    rotations = []
    for i in range(len(text)):
        rotation = text[i:] + text[:i]
        rotations.append(rotation)
    
    rotations.sort()
    
    original_idx = rotations.index(text)
    
    bwt = ''.join(rotation[-1] for rotation in rotations)
    
    return bwt, original_idx

def bwt_decode(bwt: str, original_idx: int) -> str:
    """
    Выполняет обратное преобразование Барроуза-Уилера.
    """
    if not bwt:
        return ""
        
    table = [''] * len(bwt)
    for i in range(len(bwt)):
        table = sorted([bwt[j] + table[j] for j in range(len(bwt))])
    
    return table[original_idx][:-1]

def rle_encode(text: str) -> str:
    """
    Выполняет RLE сжатие текста.
    """
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

def rle_decode(text: str) -> str:
    """
    Выполняет RLE распаковку текста.
    """
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

def compress_file(input_path: str, output_path: str) -> Tuple[int, int]:
    """
    Сжимает файл используя BWT+RLE.
    Возвращает размеры исходного и сжатого файлов.
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    bwt_text, original_idx = bwt_encode(text)
    
    compressed = rle_encode(bwt_text)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"{original_idx}\n{compressed}")
    
    return len(text.encode('utf-8')), os.path.getsize(output_path)

def decompress_file(input_path: str, output_path: str):
    """
    Распаковывает файл сжатый методом BWT+RLE.
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        original_idx = int(f.readline().strip())
        compressed = f.read()

    bwt_text = rle_decode(compressed)
    
    original = bwt_decode(bwt_text, original_idx)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(original)


input_file = 'test.txt'
compressed_file = 'test.compressed'
decompressed_file = 'test.decompressed'

original_size, compressed_size = compress_file(input_file, compressed_file)
ratio = (1 - compressed_size / original_size) * 100
print(f"Степень сжатия: {ratio:.2f}%")
print(f"Исходный размер: {original_size} байт")
print(f"Размер после сжатия: {compressed_size} байт")

decompress_file(compressed_file, decompressed_file)
print("Файл успешно распакован")
