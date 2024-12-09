import time

class SelectionSort:
    def compare(self, a, b):
        if isinstance(a, list) and isinstance(b, list):
            for x, y in zip(a, b):
                if x != y:
                    return self.compare(x, y)
            return len(a) - len(b)
        elif isinstance(a, list):
            return self.compare(a[0], b)
        elif isinstance(b, list):
            return self.compare(a, b[0])
        else:
            return -1 if str(a) < str(b) else 1 if str(a) > str(b) else 0

    def sort_nested(self, arr):
        for i in range(len(arr)):
            if isinstance(arr[i], list):
                arr[i] = self.sort_nested(arr[i])
        
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.compare(arr[j], arr[min_idx]) < 0:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    def sel_sort(self):       
        arr = self.data.copy()
        sorted_arr = self.sort_nested(arr)
        return sorted_arr

class MergeSort:
    def compare(self, a, b):
        if isinstance(a, list) and isinstance(b, list):
            for x, y in zip(a, b):
                if x != y:
                    return self.compare(x, y)
            return len(a) - len(b)
        elif isinstance(a, list):
            return self.compare(a[0], b)
        elif isinstance(b, list):
            return self.compare(a, b[0])
        else:
            return -1 if str(a) < str(b) else 1 if str(a) > str(b) else 0

    def merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if self.compare(left[i], right[j]) <= 0:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def merge_sort(self, arr):
        for i in range(len(arr)):
            if isinstance(arr[i], list):
                arr[i] = self.merge_sort(arr[i])

        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])
        return self.merge(left, right)

    def radix_sort(self): 
        arr = self.data.copy()
        sorted_arr = self.merge_sort(arr)
        return sorted_arr

class Sort(SelectionSort, MergeSort):
    def __init__(self, data=None):
        self.data = data if data is not None else []
        self.intermediate_results = []

    def sel_sort(self):
        sorted_data = super().sel_sort()
        print(f"Итоговые данные после сортировки выбором: {sorted_data}")
        return sorted_data

    def radix_sort(self):
        sorted_data = super().radix_sort()
        print(f"Итоговые данные после сортировки слиянием: {sorted_data}")
        return sorted_data

    def print_intermediate_results(self):
        print("Промежуточные результаты сортировки:")
        for step, result in enumerate(self.intermediate_results):
            print(f"Шаг {step + 1}: {result}")

class SortingData(Sort):
    def save_to_file(self, data):
        with open('sorted_data.txt', 'w') as f:
            f.write(f"Отсортированные данные: {data}\n")

    def visualize_sorting(self, sort_type):
        start = time.time()

        match sort_type:
            case 'sel':
                print("Сортировка выбором:")
                sorted_data = self.sel_sort()
            case 'radix':
                print("Сортировка слиянием:")
                sorted_data = self.radix_sort()
            case _:
                print("Неверный тип сортировки")
                return None

        end = time.time()
        finish = end - start

        if sorted_data:
            self.save_to_file(sorted_data)
            print(f"Время выполнения сортировки: {finish:.6f} секунд")
        else:
            print("Сортировка завершилась с ошибкой.")

sorter = SortingData([64, [44, 25, [1, 2, 3]], 25, ['za', 'dd'], 12, 22, 'ab', 11, 90])
sorter.visualize_sorting('sel')
sorter.visualize_sorting('radix')