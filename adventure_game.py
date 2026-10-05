import json
import random
import ollama


# =========================================================
# CONFIG
# =========================================================

MODEL = "llama3.2:latest"


# =========================================================
# WORLD
# =========================================================

LOCATIONS = [
    "Whispering Forest",
    "Pizza Kingdom",
    "Frog Academy",
    "Space Café",
    "Mystery Museum",
    "Castle of Bad Ideas",
    "Robot City",
    "Crystal Cave",
    "Sky Island",
    "Time Traveler Station",
]


STARTER_ITEMS = [
    "Magic Compass",
    "Lucky Coin",
    "Explorer Backpack",
]


# =========================================================
# OLLAMA
# =========================================================

def ask_ai(prompt):
    """
    Sends a prompt to Ollama and returns the text response.
    """

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are the Game Master of a fun, funny, safe real-life RPG adventure.

Your job is to create dynamic adventure challenges.

Rules:
- Keep the adventure suitable for teenagers.
- No dangerous real-world instructions.
- No self-harm.
- No sexual content.
- No illegal activity instructions.
- Challenges should be imaginative and game-like.
- Always provide meaningful choices.
- Choices should have different possible consequences.
- Keep descriptions short and exciting.
""",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response["message"]["content"]


# =========================================================
# JSON EXTRACTION
# =========================================================

def extract_json(text):
    """
    Extract JSON from Ollama response even if Ollama puts
    markdown/code fences around it.
    """

    if not text:
        return None

    text = text.strip()

    # Remove markdown code fences
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    # Direct JSON
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try extracting first {...}
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        possible_json = text[start:end + 1]

        try:
            return json.loads(possible_json)
        except Exception:
            pass

    return None


# =========================================================
# FALLBACK
# =========================================================

def fallback_adventure():
    """
    Used if Ollama is temporarily unavailable.
    """

    location = random.choice(LOCATIONS)

    return {
        "location": location,
        "challenge": (
            f"You arrive at {location}. "
            "Something strange is happening nearby..."
        ),
        "description": (
            "A mysterious signal appears. "
            "You need to decide what to do next."
        ),
        "choices": [
            "Investigate the signal",
            "Look around for clues",
            "Ask someone nearby for help",
            "Take a careful break and observe",
        ],
    }


# =========================================================
# CREATE FIRST ADVENTURE
# =========================================================

def create_adventure():
    """
    Creates the first AI-generated adventure.
    """

    prompt = """
Create the opening scene of a dynamic RPG.

Pick an interesting location from this list:

Whispering Forest
Pizza Kingdom
Frog Academy
Space Café
Mystery Museum
Castle of Bad Ideas
Robot City
Crystal Cave
Sky Island
Time Traveler Station

Return ONLY valid JSON in this exact structure:

{
    "location": "location name",
    "challenge": "short exciting challenge",
    "description": "short description of what is happening",
    "choices": [
        "option 1",
        "option 2",
        "option 3",
        "option 4"
    ]
}

Requirements:
- Exactly 4 choices.
- Every choice should be different.
- Choices should be fun and meaningful.
- Do not reveal which choice is best.
"""

    try:
        response = ask_ai(prompt)
        data = extract_json(response)

        if data:
            choices = data.get("choices", [])

            if isinstance(choices, list) and len(choices) >= 3:
                choices = choices[:4]

                adventure = {
                    "location": data.get(
                        "location",
                        random.choice(LOCATIONS)
                    ),
                    "challenge": data.get(
                        "challenge",
                        "A mysterious challenge appears."
                    ),
                    "description": data.get(
                        "description",
                        "Something unusual is happening."
                    ),
                    "choices": choices,
                    "history": [],
                    "inventory": STARTER_ITEMS.copy(),
                    "coins": 10,
                    "health": 100,
                    "xp": 0,
                    "turn": 1,
                    "active": True,
                    "last_event": "",
                    "last_result": "",
                    "ai_used": True,
                }

                return adventure

    except Exception as e:
        print("Ollama create error:", e)

    fallback = fallback_adventure()

    return {
        "location": fallback["location"],
        "challenge": fallback["challenge"],
        "description": fallback["description"],
        "choices": fallback["choices"],
        "history": [],
        "inventory": STARTER_ITEMS.copy(),
        "coins": 10,
        "health": 100,
        "xp": 0,
        "turn": 1,
        "active": True,
        "last_event": "",
        "last_result": "",
        "ai_used": False,
    }


# =========================================================
# GENERATE NEXT AI CHALLENGE
# =========================================================

def generate_ai_event(adventure, choice):
    """
    Ollama processes the player's choice and creates
    the result + next challenge.
    """

    history_text = "\n".join(
        [
            f"Turn {item.get('turn')}: "
            f"{item.get('choice')} -> "
            f"{item.get('result')}"
            for item in adventure.get("history", [])[-5:]
        ]
    )

    inventory_text = ", ".join(
        adventure.get("inventory", [])
    )

    prompt = f"""
You are continuing a dynamic RPG.

CURRENT GAME STATE:

Location:
{adventure.get("location")}

Current challenge:
{adventure.get("challenge")}

Current description:
{adventure.get("description")}

Player selected:
{choice}

Health:
{adventure.get("health")}

XP:
{adventure.get("xp")}

Coins:
{adventure.get("coins")}

Inventory:
{inventory_text}

Recent history:
{history_text}

Now decide what happens because of the player's choice.

Then create the NEXT challenge.

You may:
- Reward XP.
- Give coins.
- Remove coins.
- Add an item.
- Remove health.
- Restore health.
- Move the player to another location.
- Keep the same location.
- Create a funny event.
- Create a mystery.
- Create a puzzle-like challenge.
- Create a discovery.
- Create a social situation.

Keep everything safe and game-like.

Return ONLY valid JSON:

{{
    "result": "what happened because of the player's choice",
    "event": "short exciting event message",
    "xp_change": 10,
    "coin_change": 5,
    "health_change": 0,
    "item_add": "",
    "item_remove": "",
    "next_location": "location name",
    "next_challenge": "the next challenge",
    "next_description": "short description",
    "next_choices": [
        "choice 1",
        "choice 2",
        "choice 3",
        "choice 4"
    ],
    "game_over": false
}}

Important:
- next_choices must contain exactly 4 choices.
- Choices must be meaningfully different.
- Do not tell the player which choice is correct.
- xp_change should normally be between -5 and 30.
- coin_change should normally be between -10 and 30.
- health_change should normally be between -15 and 20.
- Do not create real-world dangerous instructions.
"""

    try:
        response = ask_ai(prompt)
        data = extract_json(response)

        if data:
            choices = data.get("next_choices", [])

            if isinstance(choices, list) and len(choices) >= 3:

                return {
                    "result": str(
                        data.get(
                            "result",
                            "Your choice changes the adventure."
                        )
                    ),
                    "event": str(
                        data.get(
                            "event",
                            "Something unexpected happens!"
                        )
                    ),
                    "xp_change": safe_int(
                        data.get("xp_change", 5),
                        5
                    ),
                    "coin_change": safe_int(
                        data.get("coin_change", 0),
                        0
                    ),
                    "health_change": safe_int(
                        data.get("health_change", 0),
                        0
                    ),
                    "item_add": str(
                        data.get("item_add", "")
                    ).strip(),
                    "item_remove": str(
                        data.get("item_remove", "")
                    ).strip(),
                    "next_location": str(
                        data.get(
                            "next_location",
                            adventure.get("location")
                        )
                    ),
                    "next_challenge": str(
                        data.get(
                            "next_challenge",
                            "A new challenge appears."
                        )
                    ),
                    "next_description": str(
                        data.get(
                            "next_description",
                            "Something unexpected is happening."
                        )
                    ),
                    "next_choices": choices[:4],
                    "game_over": bool(
                        data.get("game_over", False)
                    ),
                }

    except Exception as e:
        print("Ollama event error:", e)

    return fallback_result(adventure, choice)


# =========================================================
# SAFE INTEGER
# =========================================================

def safe_int(value, default=0):

    try:
        return int(value)
    except Exception:
        return default


# =========================================================
# FALLBACK RESULT
# =========================================================

def fallback_result(adventure, choice):

    events = [
        "A strange sound echoes around you.",
        "You discover something unexpected.",
        "A mysterious clue appears.",
        "The world around you suddenly becomes interesting.",
        "You successfully handle the situation.",
    ]

    location = random.choice(LOCATIONS)

    return {
        "result": f"You chose: {choice}",
        "event": random.choice(events),
        "xp_change": random.randint(5, 15),
        "coin_change": random.randint(0, 10),
        "health_change": 0,
        "item_add": "",
        "item_remove": "",
        "next_location": location,
        "next_challenge": (
            "A mysterious new challenge appears."
        ),
        "next_description": (
            "You have reached a new part of the adventure."
        ),
        "next_choices": [
            "Investigate",
            "Look for clues",
            "Try something creative",
            "Wait and observe",
        ],
        "game_over": False,
    }


# =========================================================
# PERFORM ACTION
# =========================================================

def perform_action(adventure, choice):
    """
    Main function called by app.py when player presses
    an action button.
    """

    if not adventure.get("active", True):
        return adventure

    # Save old turn
    current_turn = adventure.get("turn", 1)

    # Ask Ollama what happens
    result = generate_ai_event(
        adventure,
        choice
    )

    # -----------------------------------------
    # Save history
    # -----------------------------------------

    adventure.setdefault("history", [])

    adventure["history"].append(
        {
            "turn": current_turn,
            "choice": choice,
            "result": result["result"],
            "event": result["event"],
        }
    )

    # -----------------------------------------
    # Update stats
    # -----------------------------------------

    adventure["xp"] = max(
        0,
        adventure.get("xp", 0)
        + result["xp_change"]
    )

    adventure["coins"] = max(
        0,
        adventure.get("coins", 0)
        + result["coin_change"]
    )

    adventure["health"] = min(
        100,
        max(
            0,
            adventure.get("health", 100)
            + result["health_change"]
        )
    )

    # -----------------------------------------
    # Inventory
    # -----------------------------------------

    item_add = result.get("item_add", "").strip()

    if item_add:
        if item_add not in adventure["inventory"]:
            adventure["inventory"].append(item_add)

    item_remove = result.get("item_remove", "").strip()

    if item_remove:
        if item_remove in adventure["inventory"]:
            adventure["inventory"].remove(item_remove)

    # -----------------------------------------
    # Save result
    # -----------------------------------------

    adventure["last_result"] = result["result"]
    adventure["last_event"] = result["event"]

    # -----------------------------------------
    # Next challenge
    # -----------------------------------------

    adventure["location"] = result["next_location"]

    adventure["challenge"] = result["next_challenge"]

    adventure["description"] = result["next_description"]

    adventure["choices"] = result["next_choices"]

    adventure["turn"] = current_turn + 1

    # -----------------------------------------
    # Game over
    # -----------------------------------------

    if result.get("game_over", False):
        adventure["active"] = False

    if adventure["health"] <= 0:
        adventure["health"] = 0
        adventure["active"] = False

    return adventure
