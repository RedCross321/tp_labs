import time

class Sort:
    def __init__(self):
        self.masnum = []
        self.masstr = []

    def select_sort(self, A):
        for i in A:
            try:
                i = int(i)
                self.masnum.append(i)
            except:
                self.masstr.append(i)
            # self.masstr.append(i) if type(i) == str else self.masnum.append(i)
        return(self.sort(self.masnum) + self.sort(self.masstr))

    def sort(self, mas):
        for i in range(len(mas) - 1):
            min_index = i
            for k in range(i + 1, len(mas)):
                if mas[k] < mas[min_index]:
                    min_index = k
            mas[i], mas[min_index] = mas[min_index], mas[i]
        return mas


# data = [123456, 12345, 123456789, "d", "b", "a", 1234567, "c", 12345678]


start = time.time()

with open("sort_benchmark.txt") as file:
   data = [line.rstrip('\n\r') for line in file]

p = Sort()
data = p.select_sort(data)

with open("output.txt", "w") as file:
    file.writelines("%s\n" % k for k in data)

end = time.time()

print("Время выполнения -> ", end - start)
