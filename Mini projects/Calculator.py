
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y    

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x / y


def choice():
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    operation = input("Enter choice (1/2/3/4): ")
    return operation

def calculator():
    while True:
        operation = choice()
        if operation in ['1', '2', '3', '4']:
            try:
                num1 = int(input("Enter first number: "))
                num2 = int(input("Enter second number: "))
            except ValueError:
                print("Invalid input")
                continue

            if operation == '1':
                print(f"{num1} + {num2} = {add(num1, num2)}")
            elif operation == '2':
                print(f"{num1} - {num2} = {subtract(num1, num2)}")
            elif operation == '3':
                print(f"{num1} * {num2} = {multiply(num1, num2)}")
            elif operation == '4':
                print(f"{num1} / {num2} = {divide(num1, num2)}")
        else:
            print("Invalid")

        next_calculation = input("type yes for continue : ")
        if next_calculation.lower() != 'yes':
            break

if __name__ == "__main__":
    calculator()