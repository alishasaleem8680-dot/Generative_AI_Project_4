def calculate_average(numbers):
    total = 0

    for number in numbers:
        total += number

    average = total / len(numbers)

    print("Average:", average)

    return average


numbers = [10, 20, 30, 40]

result = calculate_average(numbers)

print("Result:", result)