import random
import json
import re
import ollama


# =========================================================
# SETTINGS
# =========================================================

MODEL = "llama3.2:latest"


# =========================================================
# GAME LOCATIONS
# =========================================================

LOCATIONS = [
    {
        "name": "🌲 Whispering Forest",
        "description": "The trees are whispering. One of them is definitely gossiping about you.",
        "choices": [
            "🌳 Talk to the suspicious tree",
            "👣 Follow the glowing footprints",
            "📦 Open the mysterious box"
        ]
    },
    {
        "name": "🍕 Pizza Kingdom",
        "description": "You have entered a kingdom where pizza is treated like gold.",
        "choices": [
            "👑 Challenge the Pizza King",
            "🍕 Enter the pizza contest",
            "🧀 Investigate the golden pizza"
        ]
    },
    {
        "name": "🐸 Frog Academy",
        "description": "A frog wearing glasses is waiting outside a very serious school.",
        "choices": [
            "🎓 Attend Frog Class",
            "🧠 Take the frog quiz",
            "🐸 Ask Professor Frog a question"
        ]
    },
    {
        "name": "🚀 Space Café",
        "description": "A café is floating in space. Somehow, nobody thinks this is strange.",
        "choices": [
            "👽 Talk to the alien waiter",
            "🍪 Order cosmic cookies",
            "🔭 Look outside the window"
        ]
    },
    {
        "name": "🕵️ Mystery Museum",
        "description": "Every statue is frozen... except one that seems to be looking directly at you.",
        "choices": [
            "🗿 Follow the moving statue",
            "🖼️ Inspect the strange painting",
            "🚪 Search for a secret door"
        ]
    },
    {
        "name": "🏰 Castle of Bad Ideas",
        "description": "A sign says: 'Welcome! Please ignore the suspicious trapdoor.'",
        "choices": [
            "🚪 Open the trapdoor",
            "🧙 Talk to the confused wizard",
            "🔎 Search the castle"
        ]
    }
]


# =========================================================
# FUNNY EVENTS
# =========================================================

FUNNY_EVENTS = [

    (
        "😂 A chicken suddenly appears and judges your decision.",
        15,
        3
    ),

    (
        "🥔 You discover a potato wearing a tiny crown.",
        20,
        4
    ),

    (
        "🤣 You tried to look heroic and walked directly into a tree.",
        10,
        2
    ),

    (
        "🐸 A frog gives you motivational advice.",
        20,
        5
    ),

    (
        "🎩 A mysterious NPC gives you a hat and disappears.",
        25,
        6
    ),

    (
        "🍕 You discover emergency pizza.",
        30,
        8
    ),

    (
        "🐔 A chicken follows you. You have no idea why.",
        15,
        3
    ),

    (
        "😎 You accidentally look extremely cool for four seconds.",
        25,
        5
    )
]


# =========================================================
# QUICK KNOWLEDGE
# =========================================================

KNOWLEDGE_FACTS = [

    "🌍 Earth is the only planet currently known to support life.",

    "🚀 A day on Venus is longer than a year on Venus.",

    "🐙 Octopuses have three hearts.",

    "🌊 The Pacific Ocean is the largest ocean on Earth.",

    "🧠 Your brain uses a surprisingly large amount of your body's energy.",

    "🌱 Plants use sunlight, water and carbon dioxide to make food.",

    "🪐 Saturn is less dense than water, so it would float in a huge enough bathtub.",

    "🐝 Bees can communicate the location of food using movements called a waggle dance.",

    "💡 Lightning can heat the surrounding air to temperatures hotter than the surface of the Sun.",

    "🦒 A giraffe has the same number of neck bones as a human: seven."
]


# =========================================================
# AI CALL
#
# IMPORTANT:
# This function is only called for special AI moments.
# =========================================================

def ask_ai(prompt):

    try:

        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a funny game master. "
                        "Use easy English. "
                        "Keep responses very short. "
                        "Make the player smile. "
                        "Do not write long explanations."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.9,
                "num_predict": 120
            }
        )

        return response["message"]["content"]

    except Exception:

        return None


# =========================================================
# JSON HELPER
# =========================================================

def extract_json(text):

    if not text:
        return None

    text = text.strip()

    text = re.sub(
        r"```json",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"```",
        "",
        text
    )

    try:

        return json.loads(text)

    except Exception:

        pass

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if match:

        try:

            return json.loads(
                match.group(0)
            )

        except Exception:

            return None

    return None


# =========================================================
# RANDOM LOCATION
# =========================================================

def get_location():

    return random.choice(
        LOCATIONS
    )


# =========================================================
# CREATE ADVENTURE
#
# NO AI CALL HERE.
# This makes game start instantly.
# =========================================================

def create_adventure():

    location = get_location()

    return {

        "location": location["name"],

        "description": location["description"],

        "choices": location["choices"],

        "history": [],

        "inventory": [],

        "coins": 0,

        "health": 100,

        "xp": 0,

        "turn": 1,

        "active": True,

        "knowledge_question": None,

        "knowledge_answered": False,

        "knowledge_correct": False,

        "last_fact": "",

        "last_event": "",

        "ai_used": False
    }


# =========================================================
# CHANGE LOCATION
#
# NO AI CALL.
# =========================================================

def next_location(adventure):

    location = get_location()

    adventure["location"] = (
        location["name"]
    )

    adventure["description"] = (
        location["description"]
    )

    adventure["choices"] = (
        location["choices"]
    )

    adventure["knowledge_question"] = None

    adventure["knowledge_answered"] = False

    adventure["knowledge_correct"] = False

    adventure["last_fact"] = ""


# =========================================================
# NORMAL FAST ACTIONS
# =========================================================

def normal_action(
    adventure,
    choice
):

    choice_lower = choice.lower()

    xp = random.randint(
        10,
        25
    )

    coins = random.randint(
        1,
        5
    )

    event = ""

    item = ""

    # -----------------------------------------------------
    # TREE
    # -----------------------------------------------------

    if "tree" in choice_lower:

        event = (
            "🌳 The tree looks at you and whispers:\n\n"
            "\"Drink water. Touch grass. Avoid suspicious trees.\"\n\n"
            "Honestly... solid advice."
        )

        xp = 25

    # -----------------------------------------------------
    # FOOTPRINTS
    # -----------------------------------------------------

    elif "footprint" in choice_lower:

        event = (
            "👣 You follow the glowing footprints..."
            "\n\n"
            "They lead to a chicken."
            "\n\n"
            "The chicken looks disappointed."
        )

        xp = 20

    # -----------------------------------------------------
    # BOX
    # -----------------------------------------------------

    elif "box" in choice_lower:

        item = "🥔 Mystery Potato"

        event = (
            "📦 You opened the mysterious box."
            "\n\n"
            "Inside: a potato."
            "\n\n"
            "Why was it locked inside a box?"
            "\n\n"
            "Nobody knows."
        )

        xp = 30

    # -----------------------------------------------------
    # PIZZA KING
    # -----------------------------------------------------

    elif "pizza king" in choice_lower:

        event = (
            "👑 The Pizza King challenges you."
            "\n\n"
            "Your weapon?"
            "\n\n"
            "A very suspicious slice of pizza."
        )

        xp = 30
        coins = 8

    # -----------------------------------------------------
    # PIZZA CONTEST
    # -----------------------------------------------------

    elif "pizza contest" in choice_lower:

        event = (
            "🍕 You enter the pizza contest."
            "\n\n"
            "You don't win."
            "\n\n"
            "But you do leave with pizza."
            "\n\n"
            "So technically... victory."
        )

        item = "🍕 Emergency Pizza"

        xp = 25

    # -----------------------------------------------------
    # GOLDEN PIZZA
    # -----------------------------------------------------

    elif "golden pizza" in choice_lower:

        event = (
            "🧀 You inspect the golden pizza."
            "\n\n"
            "It is not actually gold."
            "\n\n"
            "It's just covered in extremely expensive cheese."
        )

        coins = 10
        xp = 25

    # -----------------------------------------------------
    # FROG CLASS
    # -----------------------------------------------------

    elif "frog class" in choice_lower:

        event = (
            "🎓 Professor Frog begins the lesson."
            "\n\n"
            "\"Ribbit.\""
            "\n\n"
            "Everyone takes notes."
            "\n\n"
            "You have no idea what happened."
        )

        xp = 30

    # -----------------------------------------------------
    # FROG QUIZ
    # -----------------------------------------------------

    elif "frog quiz" in choice_lower:

        event = (
            "🐸 The frog asks you one very serious question."
            "\n\n"
            "\"What sound does a frog make?\""
            "\n\n"
            "You somehow feel nervous."
        )

        xp = 20

    # -----------------------------------------------------
    # FROG QUESTION
    # -----------------------------------------------------

    elif "professor frog" in choice_lower:

        event = (
            "🐸 Professor Frog says:"
            "\n\n"
            "\"Never underestimate small steps.\""
            "\n\n"
            "Then he jumps away."
        )

        xp = 25

    # -----------------------------------------------------
    # ALIEN
    # -----------------------------------------------------

    elif "alien" in choice_lower:

        event = (
            "👽 The alien waiter studies you carefully."
            "\n\n"
            "\"Earth human... your curiosity is acceptable.\""
            "\n\n"
            "You have no idea whether that was a compliment."
        )

        xp = 35

    # -----------------------------------------------------
    # COSMIC COOKIES
    # -----------------------------------------------------

    elif "cosmic cookie" in choice_lower:

        event = (
            "🍪 You eat a cosmic cookie."
            "\n\n"
            "For three seconds, you understand the universe."
            "\n\n"
            "Then you forget everything."
        )

        item = "🍪 Cosmic Cookie"

        xp = 30

    # -----------------------------------------------------
    # SPACE WINDOW
    # -----------------------------------------------------

    elif "window" in choice_lower:

        event = (
            "🔭 You look outside."
            "\n\n"
            "Earth looks tiny."
            "\n\n"
            "You suddenly feel very grateful for snacks."
        )

        xp = 25

    # -----------------------------------------------------
    # STATUE
    # -----------------------------------------------------

    elif "statue" in choice_lower:

        event = (
            "🗿 The statue moves."
            "\n\n"
            "You move."
            "\n\n"
            "The statue stops."
            "\n\n"
            "You stop."
            "\n\n"
            "This continues for an embarrassingly long time."
        )

        xp = 30

    # -----------------------------------------------------
    # PAINTING
    # -----------------------------------------------------

    elif "painting" in choice_lower:

        event = (
            "🖼️ You inspect the painting."
            "\n\n"
            "The person inside the painting is holding a pizza."
            "\n\n"
            "You respect this person immediately."
        )

        xp = 25

    # -----------------------------------------------------
    # SECRET DOOR
    # -----------------------------------------------------

    elif "secret door" in choice_lower:

        event = (
            "🚪 You discover a secret door."
            "\n\n"
            "You open it..."
            "\n\n"
            "It's another room."
            "\n\n"
            "Very secret. Very impressive."
        )

        xp = 30

    # -----------------------------------------------------
    # TRAPDOOR
    # -----------------------------------------------------

    elif "trapdoor" in choice_lower:

        event = (
            "🚪 You open the trapdoor."
            "\n\n"
            "A tiny wizard screams:"
            "\n\n"
            "\"I TOLD THEM THIS WAS A BAD IDEA!\""
        )

        xp = 35

    # -----------------------------------------------------
    # WIZARD
    # -----------------------------------------------------

    elif "wizard" in choice_lower:

        event = (
            "🧙 The wizard tries to cast a spell."
            "\n\n"
            "Nothing happens."
            "\n\n"
            "He says it was supposed to do that."
        )

        xp = 25

    # -----------------------------------------------------
    # CASTLE
    # -----------------------------------------------------

    elif "castle" in choice_lower:

        event = (
            "🔎 You search the castle."
            "\n\n"
            "You find 17 useless spoons."
            "\n\n"
            "This castle has serious problems."
        )

        item = "🥄 Suspicious Spoon"

        xp = 20

    # -----------------------------------------------------
    # FALLBACK
    # -----------------------------------------------------

    else:

        event = random.choice(
            FUNNY_EVENTS
        )[0]

    return (
        event,
        xp,
        coins,
        item
    )


# =========================================================
# AI SPECIAL EVENT
#
# AI IS USED ONLY SOMETIMES.
# =========================================================

def generate_ai_event(
    adventure,
    choice
):

    prompt = f"""
The player is playing a funny adventure game.

Location:
{adventure.get("location")}

Player choice:
{choice}

Create a VERY short funny reaction.

Return only JSON:

{{
    "event": "2 or 3 short funny sentences",
    "xp": 10,
    "coins": 2,
    "fact": ""
}}

Rules:

- Easy English.
- Make it genuinely funny.
- Match the player's choice.
- Do not write a long story.
- Sometimes include a useful fact.
- Most of the time fact should be empty.
"""

    result = ask_ai(
        prompt
    )

    data = extract_json(
        result
    )

    if not isinstance(
        data,
        dict
    ):

        return None

    return data


# =========================================================
# PERFORM ACTION
#
# FAST BY DEFAULT.
# AI ONLY EVERY FEW TURNS.
# =========================================================

def perform_action(
    adventure,
    choice
):

    if not isinstance(
        adventure,
        dict
    ):

        return "⚠️ Invalid adventure."

    adventure.setdefault(
        "history",
        []
    )

    adventure.setdefault(
        "inventory",
        []
    )

    adventure.setdefault(
        "health",
        100
    )

    adventure.setdefault(
        "coins",
        0
    )

    adventure.setdefault(
        "xp",
        0
    )

    adventure.setdefault(
        "turn",
        1
    )

    adventure.setdefault(
        "active",
        True
    )

    adventure.setdefault(
        "ai_used",
        False
    )

    # -----------------------------------------------------
    # HISTORY
    # -----------------------------------------------------

    adventure["history"].append(
        {
            "turn":
                adventure["turn"],

            "location":
                adventure.get(
                    "location",
                    "Unknown"
                ),

            "choice":
                choice
        }
    )

    # -----------------------------------------------------
    # SOMETIMES AI
    #
    # Every 4th turn only.
    # -----------------------------------------------------

    use_ai = (
        adventure["turn"] % 4 == 0
    )

    if use_ai:

        ai_result = generate_ai_event(
            adventure,
            choice
        )

        if ai_result:

            event = str(
                ai_result.get(
                    "event",
                    "Something strange happened."
                )
            )

            xp = ai_result.get(
                "xp",
                20
            )

            coins = ai_result.get(
                "coins",
                3
            )

            fact = str(
                ai_result.get(
                    "fact",
                    ""
                )
            )

            try:

                xp = int(xp)

            except Exception:

                xp = 20

            try:

                coins = int(coins)

            except Exception:

                coins = 3

            xp = max(
                5,
                min(40, xp)
            )

            coins = max(
                0,
                min(10, coins)
            )

            adventure["xp"] += xp

            adventure["coins"] += coins

            adventure["last_event"] = (
                f"🤖 **AI MOMENT!**\n\n"
                f"{event}\n\n"
                f"⭐ +{xp} XP\n"
                f"🪙 +{coins} coins"
            )

            if fact:

                adventure[
                    "last_fact"
                ] = fact

                adventure[
                    "last_event"
                ] += (
                    f"\n\n🧠 **You learned:**\n"
                    f"{fact}"
                )

            else:

                adventure[
                    "last_fact"
                ] = ""

            adventure["turn"] += 1

            next_location(
                adventure
            )

            return adventure[
                "last_event"
            ]

    # -----------------------------------------------------
    # FAST NORMAL ACTION
    # -----------------------------------------------------

    event, xp, coins, item = normal_action(
        adventure,
        choice
    )

    adventure["xp"] += xp

    adventure["coins"] += coins

    adventure["last_event"] = (
        f"{event}\n\n"
        f"⭐ +{xp} XP\n"
        f"🪙 +{coins} coins"
    )

    if item:

        adventure[
            "inventory"
        ].append(item)

        adventure[
            "last_event"
        ] += (
            f"\n🎒 Found: {item}"
        )

    # -----------------------------------------------------
    # RANDOM SMALL DAMAGE
    # -----------------------------------------------------

    if random.randint(
        1,
        100
    ) <= 8:

        damage = random.randint(
            3,
            8
        )

        adventure["health"] = max(
            0,
            adventure["health"]
            - damage
        )

        adventure[
            "last_event"
        ] += (
            f"\n😵 Oops! -{damage} HP"
        )

    # -----------------------------------------------------
    # TURN
    # -----------------------------------------------------

    adventure["turn"] += 1

    # -----------------------------------------------------
    # NEW LOCATION
    # -----------------------------------------------------

    next_location(
        adventure
    )

    # -----------------------------------------------------
    # GAME OVER
    # -----------------------------------------------------

    if adventure["health"] <= 0:

        adventure["active"] = False

        adventure[
            "last_event"
        ] += (
            "\n\n🏁 Adventure over!"
        )

    return adventure[
        "last_event"
    ]


# =========================================================
# KNOWLEDGE QUESTION
#
# AI is used here ONLY when specifically requested.
# =========================================================

def get_knowledge_question():

    prompt = """
Create ONE easy and interesting general knowledge question.

Return ONLY JSON:

{
    "question": "question",
    "options": [
        "option 1",
        "option 2",
        "option 3",
        "option 4"
    ],
    "answer": "correct option",
    "fact": "one short interesting fact"
}

Rules:
- Easy English.
- Exactly four options.
- One correct answer.
- Interesting for a student.
"""

    result = ask_ai(
        prompt
    )

    data = extract_json(
        result
    )

    if isinstance(
        data,
        dict
    ):

        if (
            "question" in data
            and "options" in data
            and "answer" in data
        ):

            return data

    # -----------------------------------------------------
    # FAST FALLBACK
    # -----------------------------------------------------

    return {
        "question":
            "Which planet is known as the Red Planet?",

        "options": [
            "Mars",
            "Venus",
            "Jupiter",
            "Mercury"
        ],

        "answer":
            "Mars",

        "fact":
            "Mars looks red because its surface contains iron-rich dust."
    }


# =========================================================
# CHECK KNOWLEDGE ANSWER
# =========================================================

def check_knowledge_answer(
    adventure,
    answer
):

    question = adventure.get(
        "knowledge_question"
    )

    if not question:

        return False, 0, 0

    correct = (
        answer
        == question.get(
            "answer"
        )
    )

    if correct:

        xp = 50
        coins = 10

        adventure[
            "knowledge_correct"
        ] = True

        adventure[
            "last_fact"
        ] = question.get(
            "fact",
            ""
        )

    else:

        xp = 15
        coins = 2

        adventure[
            "knowledge_correct"
        ] = False

        adventure[
            "last_fact"
        ] = (
            f"💡 Correct answer: "
            f"{question.get('answer')}\n\n"
            f"{question.get('fact', '')}"
        )

    adventure[
        "knowledge_answered"
    ] = True

    adventure["xp"] += xp

    adventure["coins"] += coins

    return (
        correct,
        xp,
        coins
    )