# Python Beginner Assessment — Homework

Five independent coding questions for a beginner student. Suggested duration:
2–3 hours. Each submission reads from standard input and writes the requested
answer to standard output. Do not print input prompts; prompt labels in the
examples are explanatory only.

Submit one Python file per question in the matching student-repository
assignment folder. See each question's JSON file for exact input and output
cases.

## Q1. Multiplication Table

Read an integer and print its multiplication table from 1 through 10, one
result per line, in the format `n x i = product`.

Topics: loops, user input.

## Q2. Remove Duplicates from a List

Read a Python-style list of integers. Create and print a new list containing
each value once, preserving the original order. Do not use `set()`.

Topics: lists, loops.

## Q3. Student Grade Calculator

Read the student's name, then integer marks for five subjects, one per line.
Assume each mark is from 0 to 100. Print the name, total, average, and grade
on separate lines using this format:

```text
Student: Asha
Total: 425
Average: 85.0
Grade: B
```

Use these grade ranges: A for 90–100, B for 80–below 90, C for 70–below 80,
D for 60–below 70, and F for below 60. Storing the information in a dictionary
is optional and is not checked by the automatic tests.

Topics: lists, dictionaries, conditionals.

## Q4. Word Frequency Counter

Read a sentence and count whitespace-separated words without regard to case.
Print each lowercase word and its count on a separate line, in order of first
appearance. Punctuation remains part of a word.

Topics: strings, dictionaries, loops.

## Q5. Number Guessing Game

Generate a random integer from 1 through 100. Read guesses until the number is
guessed. After each incorrect guess, print `Too high!` or `Too low!`. After a
correct guess, print `Correct! You guessed it in N attempts.` Count every guess
as an attempt. Do not print input prompts; output only feedback lines.

Topics: loops, conditionals, random module.

## Assessment notes

Ask the student to explain their approach, observe how they debug, and discuss
edge cases. Evaluate understanding, correctness, Python fundamentals,
readability, and problem-solving, not speed alone. The supplied tests check
program output and do not measure the rubric's conceptual or readability
criteria.
