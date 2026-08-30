import random


# =========================================================
# MEMORY OBJECTS
# =========================================================

OBJECT_POOL = [
    "🍎 Red Apple",
    "🚀 Rocket",
    "🐸 Green Frog",
    "🎸 Guitar",
    "🕶️ Sunglasses",
    "🍕 Pizza",
    "⚽ Football",
    "🦋 Butterfly",
    "🎈 Balloon",
    "☂️ Umbrella",
    "🐱 Cat",
    "🌻 Sunflower",
    "📚 Book",
    "🍩 Donut",
    "🎩 Magic Hat",
    "🧸 Teddy Bear",
    "🚲 Bicycle",
    "🎲 Dice",
    "🪄 Magic Wand",
    "🍉 Watermelon",
    "🦄 Unicorn",
    "🎧 Headphones",
    "🕯️ Candle",
    "🐼 Panda",
    "🌈 Rainbow",
    "⌚ Watch",
    "🎁 Gift Box",
    "🍔 Burger",
    "🐢 Turtle",
    "⭐ Star",
    "🧁 Cupcake",
    "🪁 Kite",
    "🔑 Golden Key",
    "🎒 Backpack",
    "🌵 Cactus",
    "🧩 Puzzle",
    "🛸 UFO",
    "🥕 Carrot",
    "🐧 Penguin",
    "🏀 Basketball",
    "🍓 Strawberry",
    "🎸 Electric Guitar",
    "🧢 Cap",
    "🦊 Fox",
    "🌙 Moon",
    "☕ Coffee Cup",
    "📷 Camera",
    "💎 Diamond",
    "🛹 Skateboard"
]


# =========================================================
# CREATE MEMORY GAME
# =========================================================

def create_memory_game():

    return random.sample(
        OBJECT_POOL,
        5
    )


# =========================================================
# CREATE MIXED OPTIONS
# =========================================================

def create_answer_options(objects):

    objects = list(objects)

    wrong_objects = [
        item
        for item in OBJECT_POOL
        if item not in objects
    ]

    # 7 fake objects
    decoys = random.sample(
        wrong_objects,
        7
    )

    options = objects + decoys

    random.shuffle(options)

    return options


# =========================================================
# CHECK MEMORY
# =========================================================

def check_memory_game(objects, selected):

    correct_objects = set(objects)

    selected_objects = set(selected)

    correct_selected = (
        correct_objects & selected_objects
    )

    wrong_selected = (
        selected_objects - correct_objects
    )

    correct_count = len(correct_selected)

    wrong_count = len(wrong_selected)

    score = max(
        0,
        correct_count - wrong_count
    )

    return min(score, 5)


# =========================================================
# MEMORY REACTION
# =========================================================

def get_memory_reaction(score):

    reactions = {

        5: [
            "🧠 PERFECT! Your brain is suspiciously powerful.",
            "🔥 5/5! Even the objects are impressed.",
            "👑 MEMORY MASTER! Your brain just flexed."
        ],

        4: [
            "😎 4/5! Almost perfect.",
            "🔥 Very sharp memory!",
            "🧠 Your brain is doing its job today."
        ],

        3: [
            "🙂 3/5! Not bad, adventurer.",
            "💪 Halfway to becoming a memory legend.",
            "🧠 Your brain needs one tiny coffee."
        ],

        2: [
            "😂 2/5! The objects successfully confused you.",
            "😅 Your brain said: 'I saw nothing.'",
            "🐸 Even the frog remembers more than this."
        ],

        1: [
            "🤣 1/5! That was more of a guessing adventure.",
            "😵 Your memory went on vacation.",
            "😂 The objects escaped your brain."
        ],

        0: [
            "💀 0/5! Your brain has left the server.",
            "😂 Absolutely nothing survived.",
            "🐔 A chicken probably remembers better."
        ]
    }

    return random.choice(
        reactions.get(
            score,
            ["Keep training!"]
        )
    )


# =========================================================
# STREAK BONUS
# =========================================================

def get_streak_bonus(streak):

    if streak >= 5:
        return 50

    if streak >= 3:
        return 30

    if streak >= 2:
        return 15

    return 0