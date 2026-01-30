# test_dummy.py

import main


def test_calculator_with_input_file():
    results = main.process_input_file("input.txt")

    assert results[0] == 15        # ADD
    assert results[1] == 16        # SUB
    assert results[2] == 21        # MUL
    assert results[3] == 4.0       # DIV
    assert results[4] == 2         # MOD

    print("All dummy tests passed ✅")


if __name__ == "__main__":
    test_calculator_with_input_file()
