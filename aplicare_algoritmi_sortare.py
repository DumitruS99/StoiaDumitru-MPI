
import time
import tracemalloc
import ast
import os
import csv

#algoritmi de sortare
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def quick_sort(arr):
    def _quick_sort(a, low, high):
        if low < high:
            pi = partition(a, low, high)
            _quick_sort(a, low, pi - 1)
            _quick_sort(a, pi + 1, high)
    def partition(a, low, high):
        pivot = a[high]
        i = low - 1
        for j in range(low, high):
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[high] = a[high], a[i + 1]
        return i + 1
    _quick_sort(arr, 0, len(arr) - 1)


def load_data_from_file(filename):
    with open(filename, 'r') as f:
        return ast.literal_eval(f.read())

def test_algorithm(algorithm, data):
    tracemalloc.start()
    start_time = time.perf_counter()
    algorithm(data.copy())
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return round(end_time - start_time, 8), round(peak / 1024, 2)


algorithms = {
    "BubbleSort": bubble_sort,
    "InsertionSort": insertion_sort,
    "QuickSort": quick_sort
}

#fisier rezultate
with open("rezultate_sortare.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Algoritm", "Fisier", "Timp (s)", "Memorie (KB)"])

    #aplicare algoritmi
    for filename in sorted(os.listdir("date_sortare")):
        filepath = os.path.join("date_sortare", filename)
        data = load_data_from_file(filepath)
        for name, algo in algorithms.items():
            print(f"Rulez {name} pe {filename}...")
            try:
                exec_time, memory_kb = test_algorithm(algo, data)
                writer.writerow([name, filename, exec_time, memory_kb])
                print(f"{name}, {filename} => {exec_time}s, {memory_kb}KB")
            except Exception as e:
                print(f"Eroare: {name}, {filename} - {e}")

print("Toate testele au fost aplicate pe datele salvate.")
