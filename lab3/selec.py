class Sort:
    def __init__(self):
        pass
    def select_sort(self, A):
        for i in range(len(A) - 1):
            min_index = i
            for k in range(i + 1, len(A)):
                if A[k] < A[min_index]:
                    min_index = k
            A[i], A[min_index] = A[min_index], A[i]
        return A


# with open("sort_benchmark.txt") as file:
#     data = [line.rstrip('\n\r') for line in file]

data = [123456, 12345, 123456789, "password", "iloveyou", "princess", 1234567, "rockyou", 12345678]
p = Sort()
data = p.select_sort(data)
print(data)

# with open("output.txt", "w") as file:
#     file.writelines("%s\n" % k for k in data)


