import random
import streamlit as st

from adventure_game import (
    create_adventure,
    perform_action,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Real Life RPG",
    page_icon="🎮",
    layout="wide",
)


# =========================================================
# MEMORY GAME DATA
# =========================================================

MEMORY_POOL = [
    "🚀 Rocket",
    "🍉 Watermelon",
    "🐱 Cat",
    "🐼 Panda",
    "🌈 Rainbow",
    "🦁 Lion",
    "🍕 Pizza",
    "⭐ Star",
]


# =========================================================
# SKILL GAME DATA
# =========================================================

SKILL_QUESTIONS = [
    {
        "question": "Which planet is known as the Red Planet?",
        "options": [
            "Mars",
            "Venus",
            "Jupiter",
            "Mercury",
        ],
        "answer": "Mars",
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": [
            "Pacific Ocean",
            "Atlantic Ocean",
            "Indian Ocean",
            "Arctic Ocean",
        ],
        "answer": "Pacific Ocean",
    },
    {
        "question": "What is the chemical formula of water?",
        "options": [
            "CO2",
            "H2O",
            "O2",
            "NaCl",
        ],
        "answer": "H2O",
    },
    {
        "question": "Which process do plants use to make food?",
        "options": [
            "Photosynthesis",
            "Digestion",
            "Respiration",
            "Evaporation",
        ],
        "answer": "Photosynthesis",
    },
    {
        "question": "How many sides does a hexagon have?",
        "options": [
            "5",
            "6",
            "7",
            "8",
        ],
        "answer": "6",
    },
]


# =========================================================
# SESSION STATE
# =========================================================

if "mode" not in st.session_state:
    st.session_state.mode = "home"

if "adventure" not in st.session_state:
    st.session_state.adventure = create_adventure()

if "memory" not in st.session_state:
    st.session_state.memory = None

if "memory_score" not in st.session_state:
    st.session_state.memory_score = 0

if "memory_round" not in st.session_state:
    st.session_state.memory_round = 0

if "skill_question" not in st.session_state:
    st.session_state.skill_question = None

if "skill_score" not in st.session_state:
    st.session_state.skill_score = 0

if "skill_result" not in st.session_state:
    st.session_state.skill_result = ""


# =========================================================
# HELPER
# =========================================================

def go_home():
    st.session_state.mode = "home"


# =========================================================
# MEMORY GAME
# =========================================================

def start_memory_round():

    shown = random.sample(
        MEMORY_POOL,
        5
    )

    decoys = [
        item
        for item in MEMORY_POOL
        if item not in shown
    ]

    decoy = random.choice(decoys)

    options = random.sample(
        shown,
        3
    )

    options.append(decoy)

    random.shuffle(options)

    st.session_state.memory = {
        "shown": shown,
        "decoy": decoy,
        "options": options,
        "phase": "show",
    }

    st.session_state.memory_round += 1


def memory_game():

    st.title("🧠 Mind Forest")

    st.caption("MEMORY QUEST")

    if st.button(
        "⬅ Back to Map",
        key="memory_back",
    ):
        go_home()
        st.rerun()

    st.divider()

    if st.session_state.memory is None:
        start_memory_round()

    memory = st.session_state.memory

    if memory["phase"] == "show":

        st.subheader("🧠 MEMORY RAID")

        st.write(
            "Remember these objects."
        )

        columns = st.columns(5)

        for i, item in enumerate(
            memory["shown"]
        ):
            with columns[i]:
                st.info(item)

        st.write("")

        if st.button(
            "I'm Ready →",
            key=f"memory_ready_{st.session_state.memory_round}",
            type="primary",
        ):
            memory["phase"] = "question"
            st.rerun()

    else:

        st.subheader(
            "Which object was NOT shown?"
        )

        st.write(
            "Choose the object that was not part "
            "of the memory set."
        )

        for i, option in enumerate(
            memory["options"]
        ):

            if st.button(
                option,
                key=(
                    f"memory_answer_"
                    f"{st.session_state.memory_round}_"
                    f"{i}"
                ),
            ):

                if option == memory["decoy"]:

                    st.session_state.memory_score += 10

                    st.success(
                        "🎉 Correct! +10 XP"
                    )

                else:

                    st.warning(
                        "Not quite! Try the next round."
                    )

                st.session_state.memory = None

                st.write(
                    f"Memory XP: "
                    f"{st.session_state.memory_score}"
                )

                st.button(
                    "Next Round",
                    key=(
                        f"memory_next_"
                        f"{st.session_state.memory_round}"
                    ),
                    on_click=start_memory_round,
                )

                st.rerun()


# =========================================================
# SKILL GAME
# =========================================================

def start_skill_question():

    st.session_state.skill_question = random.choice(
        SKILL_QUESTIONS
    )


def skill_game():

    st.title("⚔️ Skill Valley")

    st.caption("KNOWLEDGE BATTLE")

    if st.button(
        "⬅ Back to Map",
        key="skill_back",
    ):
        go_home()
        st.rerun()

    st.divider()

    if st.session_state.skill_question is None:
        start_skill_question()

    question = st.session_state.skill_question

    st.subheader(
        question["question"]
    )

    answer = st.radio(
        "Choose your answer:",
        question["options"],
        key="skill_answer",
    )

    if st.button(
        "⚔️ Submit Answer",
        key="skill_submit",
        type="primary",
    ):

        if answer == question["answer"]:

            st.session_state.skill_score += 10

            st.session_state.skill_result = (
                "🎉 Correct! +10 XP"
            )

        else:

            st.session_state.skill_result = (
                f"❌ Not quite. "
                f"The correct answer was "
                f"{question['answer']}."
            )

        st.session_state.skill_question = None

        st.rerun()

    if st.session_state.skill_result:

        st.info(
            st.session_state.skill_result
        )

    st.write(
        f"🏆 Knowledge XP: "
        f"{st.session_state.skill_score}"
    )


# =========================================================
# AI ADVENTURE
# =========================================================

def ai_adventure():

    adventure = st.session_state.adventure

    st.title("🤖 AI Adventure")

    st.caption("UNKNOWN QUEST")

    if st.button(
        "⬅ Back to Map",
        key="adventure_back",
    ):
        go_home()
        st.rerun()

    st.divider()

    # -----------------------------------------
    # Stats
    # -----------------------------------------

    stat1, stat2, stat3, stat4 = st.columns(4)

    with stat1:
        st.metric(
            "❤️ Health",
            adventure["health"],
        )

    with stat2:
        st.metric(
            "⭐ XP",
            adventure["xp"],
        )

    with stat3:
        st.metric(
            "🪙 Coins",
            adventure["coins"],
        )

    with stat4:
        st.metric(
            "🎯 Turn",
            adventure["turn"],
        )

    st.divider()

    # -----------------------------------------
    # Location
    # -----------------------------------------

    st.subheader(
        f"📍 {adventure['location']}"
    )

    st.write(
        adventure["description"]
    )

    st.divider()

    # -----------------------------------------
    # Challenge
    # -----------------------------------------

    st.subheader(
        "🎯 Your Challenge"
    )

    st.info(
        adventure["challenge"]
    )

    # -----------------------------------------
    # Last Result
    # -----------------------------------------

    if adventure.get("last_result"):

        st.subheader(
            "📜 What happened?"
        )

        st.write(
            adventure["last_result"]
        )

    if adventure.get("last_event"):

        st.success(
            adventure["last_event"]
        )

    # -----------------------------------------
    # Inventory
    # -----------------------------------------

    if adventure.get("inventory"):

        st.write(
            "🎒 Inventory: "
            + ", ".join(
                adventure["inventory"]
            )
        )

    st.divider()

    # -----------------------------------------
    # Choices
    # -----------------------------------------

    if adventure["active"]:

        st.subheader(
            "YOUR NEXT MOVE"
        )

        st.write(
            "Choose what you want to do:"
        )

        choices = adventure.get(
            "choices",
            []
        )

        for index, choice in enumerate(
            choices
        ):

            if st.button(
                choice,
                key=(
                    f"ai_choice_"
                    f"{adventure['turn']}_"
                    f"{index}"
                ),
                use_container_width=True,
            ):

                with st.spinner(
                    "🤖 Ollama is creating the result..."
                ):

                    updated_adventure = perform_action(
                        adventure,
                        choice,
                    )

                st.session_state.adventure = (
                    updated_adventure
                )

                st.rerun()

    else:

        st.warning(
            "🏁 Your adventure has ended."
        )

        st.write(
            f"Final XP: {adventure['xp']}"
        )

        st.write(
            f"Final Coins: {adventure['coins']}"
        )

        if st.button(
            "🔄 Start New AI Adventure",
            key="new_adventure",
            type="primary",
        ):

            st.session_state.adventure = (
                create_adventure()
            )

            st.rerun()


# =========================================================
# HOME / MAP
# =========================================================

def home():

    st.title("🎮 Real Life RPG")

    st.write(
        "Choose your adventure."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    # -----------------------------------------
    # MIND FOREST
    # -----------------------------------------

    with col1:

        st.subheader(
            "🧠 Mind Forest"
        )

        st.caption(
            "MEMORY QUEST"
        )

        st.write(
            "Test your memory and collect XP."
        )

        if st.button(
            "Enter Mind Forest",
            key="enter_mind",
            use_container_width=True,
        ):

            st.session_state.mode = "memory"

            st.session_state.memory = None

            st.rerun()

    # -----------------------------------------
    # AI ADVENTURE
    # -----------------------------------------

    with col2:

        st.subheader(
            "🤖 AI Adventure"
        )

        st.caption(
            "UNKNOWN QUEST"
        )

        st.write(
            "Ollama creates a new adventure "
            "for every turn."
        )

        if st.button(
            "Enter AI Adventure",
            key="enter_adventure",
            use_container_width=True,
            type="primary",
        ):

            st.session_state.mode = "adventure"

            st.session_state.adventure = (
                create_adventure()
            )

            st.rerun()

    # -----------------------------------------
    # SKILL VALLEY
    # -----------------------------------------

    with col3:

        st.subheader(
            "⚔️ Skill Valley"
        )

        st.caption(
            "KNOWLEDGE BATTLE"
        )

        st.write(
            "Answer questions and earn XP."
        )

        if st.button(
            "Enter Skill Valley",
            key="enter_skill",
            use_container_width=True,
        ):

            st.session_state.mode = "skill"

            st.session_state.skill_question = None

            st.rerun()


# =========================================================
# ROUTER
# =========================================================

if st.session_state.mode == "home":

    home()

elif st.session_state.mode == "memory":

    memory_game()

elif st.session_state.mode == "skill":

    skill_game()

elif st.session_state.mode == "adventure":

    ai_adventure()

else:

    st.session_state.mode = "home"

    st.rerun()
