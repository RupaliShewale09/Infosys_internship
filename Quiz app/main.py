import random
from quiz_db import quiz_questions

TOTAL_QUESTIONS = 5
score = 0

# Select 5 random questions
selected_questions = random.sample(quiz_questions, TOTAL_QUESTIONS)

print("\n===== Welcome to the Quiz =====")

for i, q in enumerate(selected_questions, start=1):
    print(f"\nQ{i}. {q['question']}")

    options = q["options"]
    random.shuffle(options)

    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")

    # Input validation
    while True:
        user_choice = input("Enter option number (1-4): ")
        if user_choice.isdigit() and 1 <= int(user_choice) <= 4:
            break
        print("Invalid input! Please enter a number between 1 and 4.")

    selected_option = options[int(user_choice) - 1]

    if selected_option == q["answer"]:
        print("Correct!")
        score += 1
    else:
        print("Wrong! Correct answer:", q["answer"])

# Result calculation
percentage = (score / TOTAL_QUESTIONS) * 100

print("\n===== Quiz Completed =====")
print(f"Score: {score} / {TOTAL_QUESTIONS}")
print(f"Percentage: {percentage:.2f}%")

if percentage >= 80:
    print("Performance: Excellent")
elif percentage >= 50:
    print("Performance: Good")
else:
    print("Performance: Needs Improvement")
