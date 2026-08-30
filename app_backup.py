import random


# =========================================================
# ADVENTURE WORLD
# =========================================================

WORLD = [
    {
        "name": "🌲 Whispering Forest",
        "description": (
            "A mysterious forest surrounds you. "
            "You notice glowing footprints leading in two directions."
        ),
        "knowledge": (
            "🧠 Nature Fact: Trees communicate with each other "
            "through underground fungal networks."
        ),
        "choices": [
            {
                "text": "🔎 Follow the glowing footprints",
                "type": "explore"
            },
            {
                "text": "🌳 Search the old tree",
                "type": "knowledge"
            },
            {
                "text": "🗺️ Look for a safer path",
                "type": "safe"
            }
        ]
    },

    {
        "name": "🏚️ Abandoned Cabin",
        "description": (
            "An abandoned cabin stands silently between the trees. "
            "Inside, you see a locked chest and an old notebook."
        ),
        "knowledge": (
            "🧠 History Fact: Ancient civilizations used simple locks "
            "long before modern metal keys existed."
        ),
        "choices": [
            {
                "text": "🔐 Try to open the chest",
                "type": "risk"
            },
            {
                "text": "📖 Read the old notebook",
                "type": "knowledge"
            },
            {
                "text": "🔍 Search the room",
                "type": "explore"
            }
        ]
    },

    {
        "name": "🗿 Ancient Ruins",
        "description": (
            "Huge stone ruins rise from the ground. "
            "Strange symbols cover the walls."
        ),
        "knowledge": (
            "🧠 Archaeology Fact: Archaeologists use inscriptions, "
            "artifacts and structures to understand ancient societies."
        ),
        "choices": [
            {
                "text": "🧩 Study the symbols",
                "type": "knowledge"
            },
            {
                "text": "🚪 Enter the hidden chamber",
                "type": "risk"
            },
            {
                "text": "🔎 Search the ruins",
                "type": "explore"
            }
        ]
    },

    {
        "name": "🛒 Mystery Market",
        "description": (
            "A strange market appears ahead. "
            "A mysterious merchant offers you three unusual objects."
        ),
        "knowledge": (
            "🧠 Psychology Fact: Curiosity helps humans explore "
            "and learn about unfamiliar things."
        ),
        "choices": [
            {
                "text": "🪙 Talk to the merchant",
                "type": "knowledge"
            },
            {
                "text": "🔮 Inspect the mysterious object",
                "type": "risk"
            },
            {
                "text": "🚶 Walk through the market",
                "type": "safe"
            }
        ]
    },

    {
        "name": "🌋 Crystal Cave",
        "description": (
            "You enter a glowing cave. Crystals cover the walls "
            "and something appears to be moving in the darkness."
        ),
        "knowledge": (
            "🧠 Science Fact: Crystals form when atoms or molecules "
            "arrange themselves into an organized repeating structure."
        ),
        "choices": [
            {
                "text": "💎 Examine the crystals",
                "type": "knowledge"
            },
            {
                "text": "🔥 Enter the dark tunnel",
                "type": "risk"
            },
            {
                "text": "🧭 Search for another exit",
                "type": "safe"
            }
        ]
    }
]


# =========================================================
# RANDOM ITEMS
# =========================================================

ITEMS = [
    "🗝️ Ancient Key",
    "💎 Mystery Crystal",
    "🧭 Explorer Compass",
    "📜 Ancient Scroll",
    "🪙 Golden Coin",
    "🧪 Mystery Potion",
    "🔮 Strange Orb"
]


# =========================================================
# CREATE ADVENTURE
# =========================================================

def create_adventure():

    location = random.choice(WORLD)

    return {
        "location": location["name"],
        "description": location["description"],
        "knowledge": location["knowledge"],
        "choices": location["choices"],

        "history": [],

        "inventory": [],

        "coins": 20,

        "health": 100,

        "xp": 0,

        "turn": 1,

        "active": True,

        "streak": 0,

        "knowledge_points": 0
    }


# =========================================================
# PERFORM ACTION
# =========================================================

def perform_action(adventure, choice):

    if not isinstance(adventure, dict):
        return "⚠️ Adventure data is invalid."

    # -----------------------------------------------------
    # SAFETY
    # -----------------------------------------------------

    adventure.setdefault("history", [])
    adventure.setdefault("inventory", [])
    adventure.setdefault("coins", 20)
    adventure.setdefault("health", 100)
    adventure.setdefault("xp", 0)
    adventure.setdefault("turn", 1)
    adventure.setdefault("active", True)
    adventure.setdefault("streak", 0)
    adventure.setdefault("knowledge_points", 0)

    # -----------------------------------------------------
    # FIND CHOICE TYPE
    # -----------------------------------------------------

    choice_type = "explore"

    for option in adventure.get("choices", []):

        if isinstance(option, dict):

            if option.get("text") == choice:

                choice_type = option.get(
                    "type",
                    "explore"
                )

                break

        elif option == choice:

            choice_type = "explore"

            break

    # -----------------------------------------------------
    # SAVE HISTORY
    # -----------------------------------------------------

    adventure["history"].append(
        {
            "turn": adventure["turn"],
            "location": adventure.get(
                "location",
                "Unknown"
            ),
            "choice": choice
        }
    )

    # -----------------------------------------------------
    # RANDOM EVENT
    # -----------------------------------------------------

    roll = random.randint(1, 100)

    xp = 0
    coins = 0

    event = ""

    # =====================================================
    # KNOWLEDGE CHOICE
    # =====================================================

    if choice_type == "knowledge":

        xp = random.randint(35, 60)

        adventure["knowledge_points"] += 1

        adventure["streak"] += 1

        event = (
            "🧠 KNOWLEDGE DISCOVERED!\n\n"
            f"{adventure.get('knowledge', '')}\n\n"
            f"⭐ +{xp} XP\n"
            "📚 +1 Knowledge Point"
        )

    # =====================================================
    # SAFE CHOICE
    # =====================================================

    elif choice_type == "safe":

        xp = random.randint(20, 35)

        adventure["streak"] += 1

        event = (
            "🧭 SMART MOVE!\n\n"
            "You avoided unnecessary danger "
            "and discovered a safer route.\n\n"
            f"⭐ +{xp} XP"
        )

    # =====================================================
    # RISK CHOICE
    # =====================================================

    elif choice_type == "risk":

        if roll <= 55:

            xp = random.randint(50, 80)

            coins = random.randint(10, 25)

            adventure["streak"] += 1

            event = (
                "🔥 RISK PAID OFF!\n\n"
                "Your brave decision revealed "
                "a hidden reward.\n\n"
                f"⭐ +{xp} XP\n"
                f"🪙 +{coins} coins"
            )

        else:

            health_loss = random.randint(5, 15)

            adventure["health"] = max(
                0,
                adventure["health"] - health_loss
            )

            xp = 20

            adventure["streak"] = 0

            event = (
                "⚠️ TRAP!\n\n"
                "Your decision triggered a hidden trap.\n\n"
                f"❤️ -{health_loss} Health\n"
                f"⭐ +{xp} XP"
            )

    # =====================================================
    # EXPLORE
    # =====================================================

    else:

        if roll <= 30:

            item = random.choice(ITEMS)

            xp = random.randint(30, 55)

            coins = random.randint(5, 15)

            adventure["inventory"].append(item)

            adventure["streak"] += 1

            event = (
                "✨ HIDDEN DISCOVERY!\n\n"
                f"You found: **{item}**\n\n"
                f"⭐ +{xp} XP\n"
                f"🪙 +{coins} coins"
            )

        elif roll <= 70:

            xp = random.randint(20, 40)

            adventure["streak"] += 1

            event = (
                "🔎 SOMETHING INTERESTING!\n\n"
                "You discovered clues about this place.\n\n"
                f"⭐ +{xp} XP"
            )

        else:

            health_loss = random.randint(3, 10)

            adventure["health"] = max(
                0,
                adventure["health"] - health_loss
            )

            xp = 25

            adventure["streak"] = 0

            event = (
                "🌪️ UNEXPECTED PROBLEM!\n\n"
                "The path was more dangerous than expected.\n\n"
                f"❤️ -{health_loss} Health\n"
                f"⭐ +{xp} XP"
            )

    # =====================================================
    # STREAK BONUS
    # =====================================================

    if adventure["streak"] >= 3:

        bonus = 25

        xp += bonus

        event += (
            "\n\n🔥 ADVENTURE STREAK x3!\n"
            f"⭐ Bonus +{bonus} XP"
        )

    # =====================================================
    # UPDATE REWARDS
    # =====================================================

    adventure["xp"] += xp

    adventure["coins"] += coins

    adventure["turn"] += 1

    # =====================================================
    # CHECK HEALTH
    # =====================================================

    if adventure["health"] <= 0:

        adventure["active"] = False

        event += (
            "\n\n🏁 Your adventure has ended.\n"
            "You survived as long as you could!"
        )

        return event

    # =====================================================
    # NEXT LOCATION
    # =====================================================

    new_location = random.choice(WORLD)

    adventure["location"] = new_location["name"]

    adventure["description"] = (
        new_location["description"]
    )

    adventure["knowledge"] = (
        new_location["knowledge"]
    )

    adventure["choices"] = (
        new_location["choices"]
    )

    return event


# =========================================================
# GET CHOICE TEXT
# =========================================================

def get_choice_text(choice):

    if isinstance(choice, dict):

        return choice.get(
            "text",
            "Explore"
        )

    return str(choice)


# =========================================================
# ADVENTURE SUMMARY
# =========================================================

def get_summary(adventure):

    if not isinstance(adventure, dict):

        return {
            "turns": 0,
            "items": 0,
            "knowledge": 0,
            "xp": 0,
            "coins": 0
        }

    return {
        "turns": adventure.get(
            "turn",
            1
        ),

        "items": len(
            adventure.get(
                "inventory",
                []
            )
        ),

        "knowledge": adventure.get(
            "knowledge_points",
            0
        ),

        "xp": adventure.get(
            "xp",
            0
        ),

        "coins": adventure.get(
            "coins",
            0
        )
    }