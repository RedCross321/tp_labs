def naive_search(text: str, pattern: str) -> list[int]:
    result = []
    n = len(text)
    m = len(pattern)
    
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            result.append(i)
            
    return result

def bmh_search(text: str, pattern: str) -> list[int]:
    result = []
    n = len(text)
    m = len(pattern)

    skip = {}
    for i in range(m - 1):
        skip[pattern[i]] = m - 1 - i
    
    skip_default = m
    
    i = m - 1
    while i < n:
        k = 0
        while k < m and pattern[m - 1 - k] == text[i - k]:
            k += 1
        if k == m:
            result.append(i - m + 1)
            i += 1
        else:
            char = text[i]
            i += skip.get(char, skip_default)
            
    return result



text = "ATCAGGAGATCTAGATGCCTGGAGAGGAGTGGAGAAAACGGGCATCATCATCATCCCTCTTATGGGAAGAGGTAATATGTATTTCTCCTTCGAATATAAAAAAAGTAAAAAGAAGGAAAACTTACCAAATTCACTTATGAGCCATTCATTACCCTGATACCAAAACCAGATAAAGCCCTCCACTAAAACCAAAACTGCAGCGGCGCCTTGTGGGCTCGGTCGGTTTTACTGTCCAACTCTTAATTTCAG"
pattern = "CAT"

print(f"Текст: {text}")
print(f"Паттерн: {pattern}")
print(f"Наивный алгоритм нашел вхождения на позициях: {naive_search(text, pattern)}")
print(f"BMH алгоритм нашел вхождения на позициях: {bmh_search(text, pattern)}")

