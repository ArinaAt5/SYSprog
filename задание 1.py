import multiprocessing
import time
from typing import List, Tuple

def calculate_sum_of_squares(start: int, end: int) -> int:
    total = 0
    for i in range(start, end + 1):
        total += i * i
    return total

def parallel_sum_of_squares(start: int, end: int, num_processes: int = None) -> int:

    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    # Разбиваем диапазон на поддиапазоны для каждого процесса
    total_numbers = end - start + 1
    chunk_size = total_numbers // num_processes

    ranges = []
    for i in range(num_processes):
        chunk_start = start + i * chunk_size
        chunk_end = start + (i + 1) * chunk_size - 1

        if i == num_processes - 1:
            chunk_end = end

        ranges.append((chunk_start, chunk_end))

    with multiprocessing.Pool(processes=num_processes) as pool:
        partial_sums = pool.starmap(calculate_sum_of_squares, ranges)

    total_sum = sum(partial_sums)
    return total_sum

if __name__ == "__main__":
    N = 1000000
    print(f"Вычисление суммы квадратов первых {N} натуральных чисел...")

    start_time = time.time()
    parallel_result = parallel_sum_of_squares(1, N)
    parallel_time = time.time() - start_time

    start_time = time.time()
    sequential_result = calculate_sum_of_squares(1, N)
    sequential_time = time.time() - start_time

    print(f"Результат: {parallel_result}")
    print(f"Многопроцессорное время: {parallel_time:.4f} сек")
    print(f"Последовательное время: {sequential_time:.4f} сек")
