
import ollama
import json
import random


# =========================================================
# OLLAMA SETTINGS
# =========================================================

MODEL = "llama3.2:latest"


# =========================================================
# QUESTION BANK
# =========================================================

QUESTION_BANK = [

    {
        "question": "What is the capital of India?",
        "options": [
            "Mumbai",
            "New Delhi",
            "Kolkata",
            "Chennai"
        ],
        "answer": "New Delhi",
        "explanation": "New Delhi is the capital city of India."
    },

    {
        "question": "Which planet is known as the Red Planet?",
        "options": [
            "Earth",
            "Venus",
            "Mars",
            "Jupiter"
        ],
        "answer": "Mars",
        "explanation": "Mars is called the Red Planet because of its reddish appearance."
    },

    {
        "question": "What is 12 × 8?",
        "options": [
            "86",
            "96",
            "108",
            "88"
        ],
        "answer": "96",
        "explanation": "12 multiplied by 8 equals 96."
    },

    {
        "question": "Which language is primarily used to create web page structure?",
        "options": [
            "HTML",
            "Python",
            "C++",
            "SQL"
        ],
        "answer": "HTML",
        "explanation": "HTML is used to structure the content of web pages."
    },

    {
        "question": "Which gas do humans need for respiration?",
        "options": [
            "Carbon dioxide",
            "Oxygen",
            "Hydrogen",
            "Nitrogen"
        ],
        "answer": "Oxygen",
        "explanation": "Humans need oxygen for cellular respiration."
    },

    {
        "question": "What is the largest ocean on Earth?",
        "options": [
            "Atlantic Ocean",
            "Indian Ocean",
            "Pacific Ocean",
            "Arctic Ocean"
        ],
        "answer": "Pacific Ocean",
        "explanation": "The Pacific Ocean is the largest ocean on Earth."
    },

    {
        "question": "Which data type is used for True or False in Python?",
        "options": [
            "str",
            "int",
            "bool",
            "float"
        ],
        "answer": "bool",
        "explanation": "Python uses the bool data type for True and False values."
    },

    {
        "question": "How many sides does a hexagon have?",
        "options": [
            "5",
            "6",
            "7",
            "8"
        ],
        "answer": "6",
        "explanation": "A hexagon is a polygon with six sides."
    }

]


# =========================================================
# GET QUESTION
# =========================================================

def get_question(level=1):

    """
    Returns a battle question.

    We first use the local question bank so the game
    remains fast and reliable.

    Occasionally we ask Ollama to create a new question.
    """

    # -----------------------------------------------------
    # Try AI generated question
    # -----------------------------------------------------

    try:

        prompt = f"""
You are the Quest Master of a fun educational RPG.

Create ONE multiple-choice knowledge challenge
for a player at level {level}.

The question should be interesting and suitable
for a general knowledge / logic / basic coding game.

Return ONLY valid JSON.

Required format:

{{
    "question": "question text",
    "options": [
        "option 1",
        "option 2",
        "option 3",
        "option 4"
    ],
    "answer": "exact correct option",
    "explanation": "short explanation"
}}

Important:
- Exactly 4 options.
- The answer MUST exactly match one option.
- Do not add markdown.
- Do not add extra text.
"""

        response = ollama.chat(

            model=MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )


        content = response["message"]["content"].strip()


        # -------------------------------------------------
        # Remove accidental markdown fences
        # -------------------------------------------------

        if content.startswith("```"):

            content = content.replace(
                "```json",
                ""
            )

            content = content.replace(
                "```",
                ""
            )

            content = content.strip()


        data = json.loads(content)


        # -------------------------------------------------
        # Validate AI response
        # -------------------------------------------------

        if not isinstance(data, dict):
            raise ValueError("Invalid question format")


        if "question" not in data:
            raise ValueError("Question missing")


        if "options" not in data:
            raise ValueError("Options missing")


        if "answer" not in data:
            raise ValueError("Answer missing")


        if "explanation" not in data:
            data["explanation"] = (
                "Think carefully about the concept "
                "behind this question."
            )


        if len(data["options"]) != 4:
            raise ValueError(
                "Question must have exactly 4 options"
            )


        if data["answer"] not in data["options"]:

            raise ValueError(
                "Correct answer is not one of the options"
            )


        return data


    # -----------------------------------------------------
    # Fallback
    # -----------------------------------------------------

    except Exception:

        question = random.choice(
            QUESTION_BANK
        )

        return question.copy()


# =========================================================
# CHECK ANSWER
# =========================================================

def check_answer(question, user_answer):

    if question is None:
        return False


    correct_answer = question.get(
        "answer",
        ""
    )


    return (
        str(user_answer).strip().lower()
        ==
        str(correct_answer).strip().lower()
    )


# =========================================================
# REWARD
# =========================================================

def get_reward(correct):

    if correct:

        return {

            "xp": 100,

            "coins": 10,

            "skill": 5
        }


    return {

        "xp": 20,

        "coins": 2,

        "skill": 1
    }

