def calculate(start, end):
    total = 0
    for i in range(start, end + 1):
        total = total + i * i
    return total

start = int(input("Введите стартовое значение: "))
end = int(input("Введите конечное значение: "))

result = calculate(start, end)

print(f"Сумма квадратов от {start} до {end} равна  {result}")