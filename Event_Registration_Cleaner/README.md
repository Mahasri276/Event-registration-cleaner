\# Event Registration Cleaner



\## Project Overview



Event Registration Cleaner is a Python-based application that uses an AI/LLM to extract student registration details from messy registration messages. Python is then used to clean, validate, detect duplicates, and generate reports.



\## Objective



The objective is to reduce manual work in managing college event registrations by identifying valid, incomplete, invalid, and duplicate registrations.



\## Input



The application reads student registration data from:



input/registrations.csv



The project contains 20 registration entries.



\## Information Extracted



The LLM extracts five fields:



\- Student Name

\- Phone Number

\- Email Address

\- Year

\- Branch / Department



The LLM must extract the information without inventing or correcting facts.



\## AI and Python Responsibilities



The LLM is responsible only for extracting information from unstructured registration messages and returning the result in JSON format.



Python is responsible for:



\- Cleaning names

\- Cleaning phone numbers

\- Cleaning email addresses

\- Validating phone numbers

\- Validating email addresses

\- Validating year and branch

\- Detecting duplicate registrations

\- Deciding whether an entry is VALID or NEEDS\_FIX

\- Generating reports



The system does not silently correct invalid phone numbers or email addresses.



\## Duplicate Detection



Duplicate registrations are detected after cleaning by comparing phone numbers and email addresses.



\## Testing



The project contains five normal test cases.



All five normal tests passed.



The project also contains three red-team tests:



1\. The LLM must not incorrectly fix an invalid phone number.

2\. Embedded instructions inside a registration message must be ignored.

3\. Duplicate phone numbers must be detected after cleaning.



All three red-team tests passed.



\## Output



The application generates:



\- output/clean\_list.csv

\- output/problems.csv

\- output/summary.txt



The latest full run processed 20 registrations:



\- Valid registrations: 14

\- Needs fix: 6



\## Human Review



Registrations marked as NEEDS\_FIX are reviewed by the event team. Students can be contacted when confirmation of their details is required.



\## Technologies Used



\- Python

\- Google Gemini LLM API

\- CSV

\- Visual Studio Code

\- GitHub



\## Project Files



\- main.py – Main application

\- validator.py – Cleaning and validation rules

\- llm\_extractor.py – LLM extraction

\- gemini\_client.py – Gemini connection test

\- system\_prompt.txt – LLM system instructions

\- judgment\_framework.txt – Decision-making framework

\- ai\_decision\_journal.txt – AI decision record

\- cost\_latency\_note.txt – Cost and latency notes

\- tests/test\_cases.py – Normal tests

\- tests/red\_team\_tests.py – Red-team tests

\- project\_specification.docx – Project specification

\- reflection.txt – Project reflection



\## Security



The Gemini API key is stored in a local .env file and is excluded from GitHub using .gitignore. The .env file must not be uploaded to the repository.

