import threading

def analiz(log_file):
    errors = 0
    warnings = 0

    with open(log_file, 'r') as file:
        for line in file:
            if 'ERROR' in line:
                errors += 1
            if 'WARNING' in line:
                warnings += 1

    print(f"Файл: {log_file}")
    print(f"  Ошибки: {errors}")
    print(f"  Предупреждения: {warnings}")

with open('app.log', 'w') as f:
    f.write("INFO: Start\nERROR: Problem\nWARNING: Alert\n")

with open('server.log', 'w') as f:
    f.write("ERROR: Crash\nINFO: OK\nWARNING: Slow\n")

files = ['app.log', 'server.log']
threads = []

for file in files:
    thread = threading.Thread(target=analiz, args=(file,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("Анализ завершен!")