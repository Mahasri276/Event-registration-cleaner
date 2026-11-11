
def is_valid_phone(phone):
    return (
        len(phone) == 10
        and phone.isdigit()
        and phone[0] in "6789"
    )


def is_valid_email(email):
    email = email.strip()

    if " " in email or email.count("@") != 1:
        return False

    username, domain = email.split("@")

    return (
        username != ""
        and domain != ""
        and "." in domain
        and not domain.startswith(".")
        and not domain.endswith(".")
    )


def is_valid_name(name):
    name = name.strip()

    return name != "" and any(char.isalpha() for char in name)


def is_valid_year(year):
    return year in [1, 2, 3, 4]


def is_valid_branch(branch):
    valid_branches = [
        "CSE", "IT", "AIDS", "ECE",
        "EEE", "MECH", "CIVIL"
    ]

    return branch.strip().upper() in valid_branches


def clean_phone(phone):
    phone = phone.strip()
    phone = phone.replace("+", "")
    phone = phone.replace(" ", "")
    phone = phone.replace("-", "")

    if phone.startswith("91") and len(phone) == 12:
        phone = phone[2:]

    if phone.startswith("0") and len(phone) == 11:
        phone = phone[1:]

    return phone


def clean_email(email):
    return email.strip().lower()


def clean_name(name):
    return " ".join(name.split()).title()


def clean(name, phone, email):
    return {
        "name": clean_name(name),
        "phone": clean_phone(phone),
        "email": clean_email(email)
    }


if __name__ == "__main__":

    print("Phone Number Validation")
    print(is_valid_phone("9876543210"))
    print(is_valid_phone("1234567890"))

    print("\nEmail Validation")
    print(is_valid_email("student@gmail.com"))
    print(is_valid_email("studentgmail.com"))

    print("\nName Validation")
    print(is_valid_name("Priya K"))
    print(is_valid_name(""))

    print("\nYear Validation")
    print(is_valid_year(1))
    print(is_valid_year(5))

    print("\nBranch Validation")
    print(is_valid_branch("CSE"))
    print(is_valid_branch("BIO"))

    print("\nComplete Cleaning")
    print(clean(
        "PRIYA K",
        "+91 98400 12345",
        "PRIYA.K@gmail.com"
    ))
