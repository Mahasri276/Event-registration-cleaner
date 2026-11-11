import sys
import os

# Add the main project folder to Python's path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validator import (
    clean_phone,
    clean_email,
    is_valid_phone,
    is_valid_email
)


def test_case_1():

    phone = "+91 98400 12345"

    cleaned = clean_phone(phone)

    print("Test 1 - Phone Cleaning")
    print("Input:", phone)
    print("Expected: 9840012345")
    print("Actual:", cleaned)

    if cleaned == "9840012345":
        print("PASS")
    else:
        print("FAIL")


def test_case_2():

    phone = "1234567890"

    cleaned = clean_phone(phone)

    print("\nTest 2 - Invalid Phone")
    print("Input:", phone)
    print("Valid:", is_valid_phone(cleaned))

    if not is_valid_phone(cleaned):
        print("PASS")
    else:
        print("FAIL")


def test_case_3():

    email = " PRIYA.K@gmail.com "

    cleaned = clean_email(email)

    print("\nTest 3 - Email Cleaning")
    print("Input:", email)
    print("Expected:", "priya.k@gmail.com")
    print("Actual:", cleaned)

    if cleaned == "priya.k@gmail.com":
        print("PASS")
    else:
        print("FAIL")


def test_case_4():

    email = "kavya.gmail.com"

    cleaned = clean_email(email)

    print("\nTest 4 - Invalid Email")
    print("Input:", email)
    print("Valid:", is_valid_email(cleaned))

    if not is_valid_email(cleaned):
        print("PASS")
    else:
        print("FAIL")


def test_case_5():

    phone = "9840012345"

    cleaned = clean_phone(phone)

    print("\nTest 5 - Valid Phone")
    print("Input:", phone)
    print("Valid:", is_valid_phone(cleaned))

    if is_valid_phone(cleaned):
        print("PASS")
    else:
        print("FAIL")


if __name__ == "__main__":

    print("===================================")
    print("EVENT REGISTRATION CLEANER TESTS")
    print("===================================")

    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()

    print("\n===================================")
    print("TESTING COMPLETE")
    print("===================================")