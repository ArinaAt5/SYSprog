import multiprocessing
import time
import queue
from typing import List, Tuple

def worker(input_queue: multiprocessing.Queue, output_queue: multiprocessing.Queue):
    while True:
        try:
            task = input_queue.get(timeout=1)
            if task is None:
                break

            start, end, worker_id = task
            total = 0
            for i in range(start, end + 1):
                total += i * i

            output_queue.put((worker_id, total))

        except queue.Empty:
            continue

def parallel_sum_of_squares_queues(start: int, end: int, num_processes: int = None) -> int:
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    total_numbers = end - start + 1
    chunk_size = total_numbers // num_processes

    # Создаем очереди
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    # Создаем и запускаем процессы
    processes = []
    for i in range(num_processes):
        p = multiprocessing.Process(target=worker, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    ranges = []
    for i in range(num_processes):
        chunk_start = start + i * chunk_size
        chunk_end = start + (i + 1) * chunk_size - 1

        if i == num_processes - 1:
            chunk_end = end

        input_queue.put((chunk_start, chunk_end, i))
        ranges.append((chunk_start, chunk_end))

    for _ in range(num_processes):
        input_queue.put(None)

    # Собираем результаты
    partial_sums = [0] * num_processes
    results_received = 0

    while results_received < num_processes:
        try:
            worker_id, result = output_queue.get(timeout=5)
            partial_sums[worker_id] = result
            results_received += 1
        except queue.Empty:
            print("Таймаут при получении результатов")
            break

    # Завершаем процессы
    for p in processes:
        p.join(timeout=1)
        if p.is_alive():
            p.terminate()

    # Суммируем все частичные суммы
    total_sum = sum(partial_sums)
    return total_sum

if __name__ == "__main__":
    N = 1000
    print(f"Вычисление суммы квадратов первых {N} натуральных чисел...")

    # Многопроцессорный подход с очередями
    start_time = time.time()
    parallel_result = parallel_sum_of_squares_queues(1, N)
    parallel_time = time.time() - start_time

    print(f"Результат (очереди): {parallel_result}")
    print(f"Многопроцессорное время (очереди): {parallel_time} сек")
