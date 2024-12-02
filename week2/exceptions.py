import sys

try:
    x = int(input("x: "))
    y = int(input("y: "))
except ValueError:
    print("Input must be a number")
    sys.exit(1)

try:
    result = x / y
except ZeroDivisionError:
    print("Cannot divide by 0")
    sys.exit(1)


print(result)