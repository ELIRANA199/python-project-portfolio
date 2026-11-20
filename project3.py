
import json
from pathlib import Path

QUESTIONS = [
    {
        "question": "Which language is used for Python development?",
        "options": ["A. HTML", "B. Python", "C. CSS", "D. SQL"],
        "answer": "B"
    },
    {
        "question": "Which keyword defines a function in Python?",
        "options": ["A. function", "B. define", "C. def", "D. func"],
        "answer": "C"
    },
    {
        "question": "Which data type stores True or False?",
        "options": ["A. int", "B. str", "C. list", "D. bool"],
        "answer": "D"
    },
    {
        "question": "Which symbol is used for comments in Python?",
        "options": ["A. #", "B. //", "C. <!--", "D. **"],
        "answer": "A"
    },
    {
        "question": "Which method adds an item to a list?",
        "options": ["A. add()", "B. append()", "C. insert_item()", "D. push()"],
        "answer": "B"
    }
]

RESULT_FILE = Path("quiz_results.json")


def get_answer():
    while True:
        answer = input("Your answer (A/B/C/D): ").strip().upper()

        if answer in {"A", "B", "C", "D"}:
            return answer

        print("Invalid input! Please enter A, B, C, or D.")


def run_quiz():
    score = 0
    wrong_answers = []

    print("\n===== PYTHON QUIZ =====")

    for number, question in enumerate(QUESTIONS, start=1):
        print(f"\nQuestion {number}: {question['question']}")

        for option in question["options"]:
            print(option)

        user_answer = get_answer()

        if user_answer == question["answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect! Correct answer: {question['answer']}")
            wrong_answers.append({
                "question": question["question"],
                "your_answer": user_answer,
                "correct_answer": question["answer"]
            })

    return score, wrong_answers


def save_result(score, wrong_answers):
    percentage = (score / len(QUESTIONS)) * 100

    result = {
        "score": score,
        "total_questions": len(QUESTIONS),
        "percentage": round(percentage, 2),
        "wrong_answers": wrong_answers
    }

    try:
        old_results = []

        if RESULT_FILE.exists():
            with RESULT_FILE.open("r", encoding="utf-8") as file:
                old_results = json.load(file)

            if not isinstance(old_results, list):
                raise ValueError("Invalid result file format.")

        old_results.append(result)

        with RESULT_FILE.open("w", encoding="utf-8") as file:
            json.dump(old_results, file, indent=4, ensure_ascii=False)

        print(f"\nResult saved to {RESULT_FILE.resolve()}")

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Could not save result: {error}")

    return percentage


def main():
    print("=" * 35)
    print("       PERSONAL QUIZ APP")
    print("=" * 35)

    score, wrong_answers = run_quiz()
    percentage = save_result(score, wrong_answers)

    print("\n===== FINAL RESULT =====")
    print(f"Your score: {score}/{len(QUESTIONS)}")
    print(f"Success rate: {percentage:.2f}%")

    if percentage >= 80:
        print("Excellent performance!")
    elif percentage >= 50:
        print("Good job! Keep practicing.")
    else:
        print("Keep learning and try again!")

    if wrong_answers:
        print("\nQuestions to review:")
        for item in wrong_answers:
            print(f"- {item['question']}")
            print(f"  Correct answer: {item['correct_answer']}")


if __name__ == "__main__":
    main()
