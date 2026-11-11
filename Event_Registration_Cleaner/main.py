import csv
import json
import os

from llm_extractor import extract_registration
from validator import (
    clean,
    is_valid_phone,
    is_valid_email,
    is_valid_name,
    is_valid_year,
    is_valid_branch
)


def read_entry():
    file_path = "input/registrations.csv"

    try:
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)

    except FileNotFoundError:
        print("ERROR: registrations.csv file not found.")
        return []


def check_facts(extracted):

    problems = []

    if extracted is None:
        problems.append("Gemini extraction failed")
        return problems

    if not extracted.get("name"):
        problems.append("Missing name")

    if not extracted.get("phone"):
        problems.append("Missing phone")

    if not extracted.get("email"):
        problems.append("Missing email")

    if extracted.get("year") is None:
        problems.append("Missing year")

    if not extracted.get("branch"):
        problems.append("Missing branch")

    return problems


def is_valid(extracted):

    problems = []

    name = extracted.get("name")
    phone = extracted.get("phone")
    email = extracted.get("email")
    year = extracted.get("year")
    branch = extracted.get("branch")

    if name and not is_valid_name(name):
        problems.append("Invalid name")

    cleaned_phone = clean("", phone or "", "")["phone"]

    if phone and not is_valid_phone(cleaned_phone):
        problems.append("Invalid phone")

    cleaned_email = clean("", "", email or "")["email"]

    if email and not is_valid_email(cleaned_email):
        problems.append("Invalid email")

    if year is not None:

        try:
            year_number = int(year)

            if not is_valid_year(year_number):
                problems.append("Invalid year")

        except (ValueError, TypeError):
            problems.append("Invalid year")

    if branch and not is_valid_branch(branch):
        problems.append("Invalid branch")

    return problems


def process(registrations):

    results = []

    seen_phones = set()
    seen_emails = set()

    for student in registrations:

        print("\n===================================")
        print("Processing:", student["id"])
        print("Original Entry:", student["entry"])

        extracted = extract_registration(student["entry"])

        print("\nGemini Extracted Data:")
        print(json.dumps(extracted, indent=4))

        if extracted is None:

            results.append({
                "id": student["id"],
                "status": "NEEDS_FIX",
                "name": "",
                "phone": "",
                "email": "",
                "year": "",
                "branch": "",
                "reasons": "Gemini extraction failed",
                "original_entry": student["entry"]
            })

            continue

        fact_problems = check_facts(extracted)

        validation_problems = is_valid(extracted)

        all_problems = fact_problems + validation_problems

        cleaned = clean(
            extracted.get("name", ""),
            extracted.get("phone", ""),
            extracted.get("email", "")
        )

        cleaned_name = cleaned["name"]
        cleaned_phone = cleaned["phone"]
        cleaned_email = cleaned["email"]

        if cleaned_phone:

            if cleaned_phone in seen_phones:
                all_problems.append("Duplicate phone")
            else:
                seen_phones.add(cleaned_phone)

        if cleaned_email:

            if cleaned_email in seen_emails:
                all_problems.append("Duplicate email")
            else:
                seen_emails.add(cleaned_email)

        if all_problems:
            status = "NEEDS_FIX"
        else:
            status = "VALID"

        results.append({
            "id": student["id"],
            "status": status,
            "name": cleaned_name,
            "phone": cleaned_phone,
            "email": cleaned_email,
            "year": extracted.get("year"),
            "branch": extracted.get("branch", "").strip().upper(),
            "reasons": "; ".join(all_problems),
            "original_entry": student["entry"]
        })

    return results


def write_reports(results):

    os.makedirs("output", exist_ok=True)

    clean_file = "output/clean_list.csv"
    problems_file = "output/problems.csv"
    summary_file = "output/summary.txt"

    valid_records = []
    problem_records = []

    for result in results:

        if result["status"] == "VALID":
            valid_records.append(result)
        else:
            problem_records.append(result)

    # -----------------------------
    # CLEAN LIST
    # -----------------------------

    with open(
        clean_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "id",
            "name",
            "phone",
            "email",
            "year",
            "branch"
        ])

        for result in valid_records:

            writer.writerow([
                result["id"],
                result["name"],
                result["phone"],
                result["email"],
                result["year"],
                result["branch"]
            ])

    # -----------------------------
    # PROBLEMS
    # -----------------------------

    with open(
        problems_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "id",
            "status",
            "reasons",
            "original_entry"
        ])

        for result in problem_records:

            writer.writerow([
                result["id"],
                result["status"],
                result["reasons"],
                result["original_entry"]
            ])

    # -----------------------------
    # SUMMARY
    # -----------------------------

    branch_counts = {}
    year_counts = {}

    for result in valid_records:

        branch = result["branch"]
        year = result["year"]

        branch_counts[branch] = branch_counts.get(branch, 0) + 1
        year_counts[year] = year_counts.get(year, 0) + 1

    with open(
        summary_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("EVENT REGISTRATION CLEANER SUMMARY\n")
        file.write("=================================\n\n")

        file.write(
            f"Total registrations: {len(results)}\n"
        )

        file.write(
            f"Valid registrations: {len(valid_records)}\n"
        )

        file.write(
            f"Needs fix: {len(problem_records)}\n\n"
        )

        file.write("Valid registrations by branch:\n")

        for branch, count in sorted(branch_counts.items()):
            file.write(f"{branch}: {count}\n")

        file.write("\nValid registrations by year:\n")

        for year, count in sorted(year_counts.items()):
            file.write(f"Year {year}: {count}\n")

    print("\n===================================")
    print("REPORTS CREATED")
    print("===================================")
    print("clean_list.csv created")
    print("problems.csv created")
    print("summary.txt created")


def main():

    print("===================================")
    print("   EVENT REGISTRATION CLEANER")
    print("===================================")

    registrations = read_entry()

    if not registrations:
        return

    print("\nTotal registrations:", len(registrations))

    results = process(registrations)

    valid_count = sum(
        1
        for result in results
        if result["status"] == "VALID"
    )

    needs_fix_count = sum(
        1
        for result in results
        if result["status"] == "NEEDS_FIX"
    )

    print("\n===================================")
    print("PROCESSING COMPLETE")
    print("===================================")

    print("Valid registrations:", valid_count)
    print("Needs fix:", needs_fix_count)

    write_reports(results)


if __name__ == "__main__":
    main()