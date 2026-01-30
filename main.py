# main.py

from calculator import add, subtract, multiply, divide, modulus


def process_input_file(file_path):
    results = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            operation, a, b = line.split()
            a = float(a)
            b = float(b)

            if operation == "ADD":
                result = add(a, b)
            elif operation == "SUB":
                result = subtract(a, b)
            elif operation == "MUL":
                result = multiply(a, b)
            elif operation == "DIV":
                result = divide(a, b)
            elif operation == "MOD":
                result = modulus(a, b)
            else:
                raise ValueError(f"Invalid operation: {operation}")

            results.append(result)

    return results


if __name__ == "__main__":
    input_file = "input.txt"
    output = process_input_file(input_file)

    for res in output:
        print(res)
