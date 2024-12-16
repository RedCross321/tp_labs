import time

def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    occurrences = []
    
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            occurrences.append(i)
            
    return occurrences

def build_bad_match_table(pattern):
    bad_match = {}
    pattern_length = len(pattern)
    
    # Заполняем таблицу для всех символов в паттерне
    for i in range(pattern_length - 1):
        bad_match[pattern[i]] = pattern_length - 1 - i
        
    # Для всех остальных символов значение равно длине паттерна
    return lambda x: bad_match.get(x, pattern_length)

def bmh_search(text, pattern):
    occurrences = []
    pattern_length = len(pattern)
    text_length = len(text)
    
    if pattern_length > text_length:
        return occurrences
    
    bad_match = build_bad_match_table(pattern)
    
    shift = 0
    while shift <= text_length - pattern_length:
        mismatch = False
        
        for i in range(pattern_length - 1, -1, -1):
            if pattern[i] != text[shift + i]:
                mismatch = True
                break
                
        if not mismatch:
            occurrences.append(shift)
            shift += 1
        else:
            shift += bad_match(text[shift + pattern_length - 1])
            
    return occurrences

def find_longest_cat_sequence(file_path):
    # Чтение FASTA файла
    try:
        with open(file_path, 'r') as file:
            # Пропускаем заголовок FASTA
            header = file.readline()
            # Читаем последовательность
            sequence = ''.join(line.strip() for line in file)
            
        # Поиск самой длинной последовательности CAT
        max_length = 0
        test_pattern = "CAT"
        
        while test_pattern in sequence:
            max_length += 1
            test_pattern += "CAT"
        
        # Берем последнюю успешную длину
        final_pattern = "CAT" * max_length
        
        # Измеряем время для наивного алгоритма
        start_time = time.time()
        naive_results = naive_search(sequence, final_pattern)
        naive_time = time.time() - start_time
        
        # Измеряем время для алгоритма БМХ
        start_time = time.time()
        bmh_results = bmh_search(sequence, final_pattern)
        bmh_time = time.time() - start_time
        
        return {
            'pattern_length': len(final_pattern),
            'occurrences': len(naive_results),
            'positions': naive_results,
            'naive_time': naive_time,
            'bmh_time': bmh_time
        }
        
    except FileNotFoundError:
        return f"Файл {file_path} не найден"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

def main():
    file_path = "Felis_catus.Felis_catus_9.0.dna.chromosome.A1.fa"
    results = find_longest_cat_sequence(file_path)
    
    if isinstance(results, dict):
        print(f"\nРезультаты поиска:")
        print(f"Длина найденной последовательности CAT: {results['pattern_length']} символов")
        print(f"Количество найденных вхождений: {results['occurrences']}")
        print(f"Позиции вхождений: {results['positions']}")
        print(f"\nВремя выполнения:")
        print(f"Наивный алгоритм: {results['naive_time']:.4f} секунд")
        print(f"Алгоритм БМХ: {results['bmh_time']:.4f} секунд")
    else:
        print(results)

if __name__ == "__main__":
    main()