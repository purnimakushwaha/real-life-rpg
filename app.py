import streamlit as st
import re
import html

from database import (
    init_db,
    create_player,
    get_player,
    save_player
)

from mini_games import (
    create_memory_game,
    create_answer_options,
    check_memory_game
)

from skill_game import (
    get_question,
    check_answer,
    get_reward
)

from adventure_game import (
    create_adventure,
    perform_action
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Real Life RPG",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CSS ONLY
# NO HTML CONTENT WILL BE USED FOR GAME TEXT
# =========================================================

st.markdown(
    """
    <style>

    html, body, [class*="css"] {
        font-family: Arial, sans-serif;
    }

    .block-container {
        max-width: 1500px !important;
        padding-top: 1.5rem !important;
        padding-left: 4vw !important;
        padding-right: 4vw !important;
        padding-bottom: 3rem !important;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                circle at 15% 15%,
                rgba(80,90,220,0.22),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 25%,
                rgba(0,190,210,0.16),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 90%,
                rgba(120,60,180,0.16),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #050713,
                #0b1024,
                #070914
            );

        min-height: 100vh;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    footer {
        visibility: hidden;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }

    [data-testid="stDecoration"] {
        display: none;
    }

    .game-title {
        font-size: 46px;
        font-weight: 900;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 5px;
        letter-spacing: 2px;
        text-shadow: 0 0 25px rgba(120,140,255,0.35);
    }

    .game-subtitle {
        text-align: center;
        font-size: 17px;
        color: #aeb7d8;
        margin-bottom: 30px;
    }

    .card {
        padding: 25px;
        border-radius: 24px;
        margin-bottom: 20px;
        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.09),
                rgba(255,255,255,0.025)
            );
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 18px 50px rgba(0,0,0,0.35);
    }

    .hud-box {
        text-align: center;
        padding: 18px 10px;
        border-radius: 20px;
        background: rgba(255,255,255,0.065);
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 10px 30px rgba(0,0,0,0.20);
    }

    .hud-icon {
        font-size: 23px;
    }

    .hud-number {
        font-size: 25px;
        font-weight: 900;
        margin-top: 3px;
    }

    .hud-label {
        font-size: 11px;
        letter-spacing: 1.5px;
        color: #9fa9cf;
        margin-top: 3px;
    }

    .location-title {
        font-size: 30px;
        font-weight: 900;
        margin-bottom: 7px;
    }

    .location-description {
        font-size: 17px;
        color: #cbd2eb;
        line-height: 1.5;
    }

    .mission-box {
        padding: 22px;
        border-radius: 22px;
        margin: 20px 0;
        background:
            linear-gradient(
                135deg,
                rgba(80,90,190,0.20),
                rgba(20,150,170,0.10)
            );
        border: 1px solid rgba(255,255,255,0.12);
    }

    .mission-label {
        font-size: 13px;
        letter-spacing: 2px;
        color: #9fa9cf;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .mission-text {
        font-size: 24px;
        font-weight: 850;
    }

    .event-box {
        padding: 24px;
        border-radius: 22px;
        margin: 20px 0;
        background:
            linear-gradient(
                135deg,
                rgba(255,190,70,0.10),
                rgba(120,70,180,0.10)
            );
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 15px 40px rgba(0,0,0,0.30);
    }

    .event-label {
        font-size: 13px;
        letter-spacing: 2px;
        color: #aeb7d8;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .event-text {
        font-size: 18px;
        line-height: 1.65;
        color: #f5f7ff;
    }

    .reward-box {
        display: inline-block;
        padding: 9px 15px;
        margin: 8px 8px 0 0;
        border-radius: 14px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.10);
        font-weight: 800;
    }

    .map-title {
        font-size: 27px;
        font-weight: 900;
    }

    .map-small {
        font-size: 12px;
        letter-spacing: 2px;
        color: #9fa9cf;
        margin-top: 5px;
    }

    .stButton > button {
        width: 100%;
        min-height: 60px;
        border-radius: 17px !important;
        border: 1px solid rgba(255,255,255,0.13) !important;
        background: rgba(255,255,255,0.07) !important;
        color: white !important;
        font-size: 15px !important;
        font-weight: 750 !important;
        transition: 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        background: rgba(255,255,255,0.14) !important;
        box-shadow: 0 12px 30px rgba(0,0,0,0.30);
    }

    .stTextInput input {
        border-radius: 15px !important;
        background: rgba(255,255,255,0.07) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }

    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.065);
        padding: 15px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.09);
    }

    @media (max-width: 700px) {

        .game-title {
            font-size: 34px;
        }

        .location-title {
            font-size: 25px;
        }

        .mission-text {
            font-size: 20px;
        }

        .event-text {
            font-size: 16px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DATABASE
# =========================================================

init_db()


# =========================================================
# SESSION STATE
# =========================================================

defaults = {

    "screen": "welcome",
    "name": "",

    "xp": 0,
    "coins": 0,
    "level": 1,

    "mind": 0,
    "skill": 0,
    "discipline": 0,
    "creativity": 0,

    "completed": 0,

    # MEMORY
    "memory_objects": [],
    "memory_options": [],
    "memory_selected": [],
    "memory_phase": "ready",
    "memory_score": 0,
    "memory_reward": 0,
    "memory_result": "",

    # SKILL
    "skill_question": None,
    "skill_answered": False,
    "skill_correct": False,
    "skill_reward": 0,
    "skill_monster": None,
    "skill_hp": 100,
    "skill_selected_answer": "",

    # ADVENTURE
    "adventure": None,
    "adventure_event": ""
}


for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# SAVE PROGRESS
# =========================================================

def save_progress():

    save_player({

        "name": st.session_state.name,
        "xp": st.session_state.xp,
        "coins": st.session_state.coins,
        "level": st.session_state.level,

        "mind": st.session_state.mind,
        "skill": st.session_state.skill,
        "discipline": st.session_state.discipline,
        "creativity": st.session_state.creativity,

        "completed": st.session_state.completed,

        "streak": 0,
        "last_quest_date": None
    })


# =========================================================
# LOAD PLAYER
# =========================================================

def load_player(name):

    player = get_player(name)

    if player is None:

        create_player(name)
        player = get_player(name)

    if player:

        for key, value in player.items():

            if key in st.session_state:
                st.session_state[key] = value


# =========================================================
# LEVEL SYSTEM
# =========================================================

def update_level():

    st.session_state.level = (
        st.session_state.xp // 500
    ) + 1


# =========================================================
# MEMORY GAME
# =========================================================

def start_memory():

    objects = create_memory_game()

    options = create_answer_options(objects)

    st.session_state.memory_objects = objects
    st.session_state.memory_options = options
    st.session_state.memory_selected = []
    st.session_state.memory_score = 0
    st.session_state.memory_reward = 0
    st.session_state.memory_result = ""
    st.session_state.memory_phase = "memorize"
    st.session_state.screen = "memory"


def finish_memory():

    score = check_memory_game(
        st.session_state.memory_objects,
        st.session_state.memory_selected
    )

    st.session_state.memory_score = score

    if score == 5:

        xp = 150
        coins = 15
        result = "🏆 PERFECT MEMORY!"

    elif score == 4:

        xp = 120
        coins = 12
        result = "🔥 AMAZING!"

    elif score == 3:

        xp = 80
        coins = 8
        result = "⚡ GOOD JOB!"

    elif score == 2:

        xp = 50
        coins = 5
        result = "🙂 NOT BAD!"

    else:

        xp = 30
        coins = 3
        result = "💪 KEEP TRAINING!"

    st.session_state.xp += xp
    st.session_state.coins += coins

    st.session_state.mind = min(
        100,
        st.session_state.mind + score * 2
    )

    st.session_state.completed += 1

    st.session_state.memory_reward = xp
    st.session_state.memory_result = result
    st.session_state.memory_phase = "result"

    update_level()
    save_progress()


# =========================================================
# SKILL VALLEY
# =========================================================

def start_skill():

    monsters = [

        ("👾", "Code Monster"),
        ("🐉", "Math Dragon"),
        ("👺", "Logic Goblin"),
        ("🧙", "Knowledge Wizard")
    ]

    monster = monsters[
        len(st.session_state.name) % len(monsters)
    ]

    st.session_state.skill_question = None
    st.session_state.skill_monster = monster
    st.session_state.skill_hp = 100
    st.session_state.skill_answered = False
    st.session_state.skill_correct = False
    st.session_state.skill_reward = 0
    st.session_state.skill_selected_answer = ""

    st.session_state.screen = "skill"


def answer_skill(answer):

    question = st.session_state.skill_question

    if question is None:
        return

    correct = check_answer(question, answer)

    reward = get_reward(correct)

    st.session_state.skill_answered = True
    st.session_state.skill_correct = correct
    st.session_state.skill_reward = reward["xp"]
    st.session_state.skill_selected_answer = answer

    if correct:
        st.session_state.skill_hp = 0
    else:
        st.session_state.skill_hp = 100

    st.session_state.xp += reward["xp"]
    st.session_state.coins += reward["coins"]

    st.session_state.skill = min(
        100,
        st.session_state.skill + reward["skill"]
    )

    st.session_state.completed += 1

    update_level()
    save_progress()


# =========================================================
# START ADVENTURE
# =========================================================

def start_adventure():

    try:

        adventure = create_adventure()

        if not isinstance(adventure, dict):
            adventure = None

        if adventure is None:

            adventure = {

                "location": "🌲 Whispering Forest",

                "description":
                    "Something suspicious is moving behind the trees.",

                "choices": [
                    "🔎 Investigate the noise",
                    "🌳 Talk to the tree",
                    "🏃 Run away dramatically"
                ],

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
                "last_event": ""
            }

        adventure.setdefault("history", [])
        adventure.setdefault("inventory", [])
        adventure.setdefault("coins", 0)
        adventure.setdefault("health", 100)
        adventure.setdefault("xp", 0)
        adventure.setdefault("turn", 1)
        adventure.setdefault("active", True)

        adventure.setdefault(
            "knowledge_question",
            None
        )

        adventure.setdefault(
            "knowledge_answered",
            False
        )

        adventure.setdefault(
            "knowledge_correct",
            False
        )

        adventure.setdefault(
            "last_fact",
            ""
        )

        adventure.setdefault(
            "last_event",
            ""
        )

        st.session_state.adventure = adventure
        st.session_state.adventure_event = ""
        st.session_state.screen = "ai_adventure"

    except Exception as e:

        st.error(
            "⚠️ Could not start the AI Adventure."
        )

        st.code(str(e))


# =========================================================
# ADVENTURE ACTION
# =========================================================

def adventure_action(choice):

    adventure = st.session_state.adventure

    if not isinstance(adventure, dict):

        start_adventure()
        return

    old_xp = adventure.get("xp", 0)
    old_coins = adventure.get("coins", 0)

    try:

        event = perform_action(
            adventure,
            choice
        )

        st.session_state.adventure_event = event

        new_xp = adventure.get("xp", 0)
        new_coins = adventure.get("coins", 0)

        earned_xp = max(
            0,
            new_xp - old_xp
        )

        earned_coins = max(
            0,
            new_coins - old_coins
        )

        st.session_state.xp += earned_xp
        st.session_state.coins += earned_coins

        adventure["xp"] = 0
        adventure["coins"] = 0

        st.session_state.completed += 1

        update_level()
        save_progress()

    except Exception as e:

        st.session_state.adventure_event = (
            "⚠️ Something unexpected happened."
        )

        st.error(str(e))


# =========================================================
# CLEAN AI EVENT
# =========================================================

def clean_event_text(event):

    if not event:
        return "", []

    text = str(event)

    # Remove HTML comments
    text = re.sub(
        r"<!--.*?-->",
        "",
        text,
        flags=re.DOTALL
    )

    # Remove code fences
    text = re.sub(
        r"```(?:html|HTML|markdown|Markdown|text|TEXT)?",
        "",
        text
    )

    text = text.replace("```", "")

    # Remove HTML tags
    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    # Decode HTML entities
    text = html.unescape(text)

    # Remove CSS/class fragments
    bad_phrases = [
        "mission-label",
        "mission-text",
        "event-label",
        "event-text",
        "location-title",
        "location-description",
        "hud-icon",
        "hud-number",
        "hud-label",
        "map-icon",
        "map-title",
        "map-small",
        "WHAT JUST HAPPENED",
        "YOUR NEXT MOVE"
    ]

    for phrase in bad_phrases:
        text = text.replace(phrase, "")

    # Remove markdown headings
    text = re.sub(
        r"^\s*#{1,6}\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    # Remove excessive blank lines
    text = re.sub(
        r"\n\s*\n\s*\n+",
        "\n\n",
        text
    )

    text = text.strip()

    lines = text.splitlines()

    main_lines = []
    rewards = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Ignore pure HTML leftovers
        if line in ["div", "/div", "span", "/span"]:
            continue

        # Reward lines
        if (
            re.search(r"\+\s*\d+\s*XP", line, re.I)
            or
            re.search(r"\+\s*\d+\s*coins?", line, re.I)
        ):

            rewards.append(line)

        else:

            main_lines.append(line)

    return "\n\n".join(main_lines), rewards


# =========================================================
# WELCOME
# =========================================================

if st.session_state.screen == "welcome":

    st.markdown(
        '<div class="game-title">🎮 REAL LIFE RPG</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="game-subtitle">'
        'Your everyday life just became a game.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("## 🌎 Welcome, Adventurer!")

    st.write(
        "Explore strange places, beat challenges, "
        "collect XP and discover ridiculous surprises."
    )

    name = st.text_input(
        "👤 What should we call you?",
        placeholder="Enter your name..."
    )

    if st.button(
        "🚀 START GAME",
        use_container_width=True
    ):

        if not name.strip():

            st.warning(
                "Please enter your name."
            )

        else:

            load_player(name.strip())

            st.session_state.screen = "home"

            st.rerun()


# =========================================================
# HOME / WORLD MAP
# =========================================================

elif st.session_state.screen == "home":

    st.markdown(
        '<div class="game-title">'
        f'👋 {st.session_state.name}'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="game-subtitle">'
        'Welcome back, Adventurer.'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # HUD
    # -----------------------------------------------------

    h1, h2, h3, h4 = st.columns(4)

    with h1:

        st.markdown(
            f"""
            <div class="hud-box">
                <div class="hud-icon">👑</div>
                <div class="hud-number">
                    {st.session_state.level}
                </div>
                <div class="hud-label">LEVEL</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with h2:

        st.markdown(
            f"""
            <div class="hud-box">
                <div class="hud-icon">⭐</div>
                <div class="hud-number">
                    {st.session_state.xp}
                </div>
                <div class="hud-label">XP</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with h3:

        st.markdown(
            f"""
            <div class="hud-box">
                <div class="hud-icon">🪙</div>
                <div class="hud-number">
                    {st.session_state.coins}
                </div>
                <div class="hud-label">COINS</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with h4:

        st.markdown(
            f"""
            <div class="hud-box">
                <div class="hud-icon">🏆</div>
                <div class="hud-number">
                    {st.session_state.completed}
                </div>
                <div class="hud-label">QUESTS</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.markdown("## 🗺️ YOUR WORLD")
    st.caption("Choose your next destination.")

    c1, c2, c3 = st.columns(3)

    # -----------------------------------------------------
    # MIND FOREST
    # -----------------------------------------------------

    with c1:

        st.markdown("## 🧠 Mind Forest")

        st.caption("MEMORY QUEST")

        st.write(
            "A forest where your memory gets tested."
        )

        if st.button(
            "🌲 ENTER FOREST",
            key="home_memory",
            use_container_width=True
        ):

            start_memory()
            st.rerun()

    # -----------------------------------------------------
    # AI ADVENTURE
    # -----------------------------------------------------

    with c2:

        st.markdown("## 🤖 AI Adventure")

        st.caption("UNKNOWN QUEST")

        st.write(
            "Strange places, weird characters "
            "and unexpected events."
        )

        if st.button(
            "🚀 ENTER ADVENTURE",
            key="home_adventure",
            use_container_width=True
        ):

            start_adventure()
            st.rerun()

    # -----------------------------------------------------
    # SKILL VALLEY
    # -----------------------------------------------------

    with c3:

        st.markdown("## ⚔️ Skill Valley")

        st.caption("KNOWLEDGE BATTLE")

        st.write(
            "Fight monsters using your knowledge."
        )

        if st.session_state.level < 3:

            st.button(
                "🔒 UNLOCK AT LEVEL 3",
                key="locked_skill",
                disabled=True,
                use_container_width=True
            )

        else:

            if st.button(
                "⚔️ ENTER VALLEY",
                key="home_skill",
                use_container_width=True
            ):

                start_skill()
                st.rerun()

    st.write("")

    if st.button(
        "🧙 VIEW CHARACTER",
        use_container_width=True
    ):

        st.session_state.screen = "character"
        st.rerun()


# =========================================================
# MEMORY GAME
# =========================================================

elif st.session_state.screen == "memory":

    phase = st.session_state.memory_phase

    # -----------------------------------------------------
    # MEMORIZE
    # -----------------------------------------------------

    if phase == "memorize":

        st.markdown(
            '<div class="game-title">🧠 MEMORY RAID</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="game-subtitle">'
            'Your brain has 5 seconds of fame.'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("## 👀 Remember these objects!")

        cols = st.columns(5)

        for i, item in enumerate(
            st.session_state.memory_objects
        ):

            parts = item.split(" ", 1)

            with cols[i]:

                st.markdown(
                    f"### {parts[0]}"
                )

                if len(parts) > 1:
                    st.write(parts[1])

        st.write("")

        if st.button(
            "🙈 HIDE OBJECTS",
            use_container_width=True
        ):

            st.session_state.memory_phase = "answer"
            st.rerun()

    # -----------------------------------------------------
    # ANSWER
    # -----------------------------------------------------

    elif phase == "answer":

        st.markdown(
            '<div class="game-title">🔍 MEMORY TEST</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="game-subtitle">'
            'Find the 5 objects you actually saw.'
            '</div>',
            unsafe_allow_html=True
        )

        selected_count = len(
            st.session_state.memory_selected
        )

        st.info(
            f"🎯 Selected: {selected_count}/5"
        )

        options = st.session_state.memory_options

        cols = st.columns(2)

        for i, item in enumerate(options):

            selected = (
                item in
                st.session_state.memory_selected
            )

            label = (
                f"✅ {item}"
                if selected
                else f"⬜ {item}"
            )

            with cols[i % 2]:

                if st.button(
                    label,
                    key=f"memory_option_{i}",
                    use_container_width=True
                ):

                    if selected:

                        st.session_state.memory_selected.remove(
                            item
                        )

                    else:

                        if selected_count < 5:

                            st.session_state.memory_selected.append(
                                item
                            )

                        else:

                            st.warning(
                                "You already selected 5."
                            )

                    st.rerun()

        if len(
            st.session_state.memory_selected
        ) == 5:

            st.write("")

            if st.button(
                "⚔️ LOCK ANSWERS",
                use_container_width=True
            ):

                finish_memory()
                st.rerun()

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    elif phase == "result":

        st.markdown(
            f'<div class="game-title">'
            f'{st.session_state.memory_result}'
            f'</div>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "🧠 SCORE",
                f"{st.session_state.memory_score}/5"
            )

        with c2:

            st.metric(
                "⭐ XP EARNED",
                f"+{st.session_state.memory_reward}"
            )

        st.write("")

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "🔄 PLAY AGAIN",
                use_container_width=True
            ):

                start_memory()
                st.rerun()

        with c2:

            if st.button(
                "🗺️ BACK TO MAP",
                use_container_width=True
            ):

                st.session_state.screen = "home"
                st.rerun()


# =========================================================
# AI ADVENTURE
# =========================================================

elif st.session_state.screen == "ai_adventure":

    adventure = st.session_state.adventure

    if not isinstance(adventure, dict):

        start_adventure()
        st.rerun()

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    st.markdown(
        '<div class="game-title">🤖 AI ADVENTURE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="game-subtitle">'
        f'Turn {adventure.get("turn", 1)} '
        '• The world has no idea what happens next.'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # ADVENTURE HUD
    # -----------------------------------------------------

    h1, h2, h3 = st.columns(3)

    with h1:

        st.markdown(
            f"""
            <div class="hud-box">
                <div class="hud-icon">❤️</div>
                <div class="hud-number">
                    {adventure.get("health", 100)}
                </div>
                <div class="hud-label">HEALTH</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with h2:

        st.markdown(
            f"""
            <div class="hud-box">
                <div class="hud-icon">🪙</div>
                <div class="hud-number">
                    {adventure.get("coins", 0)}
                </div>
                <div class="hud-label">COINS</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with h3:

        st.markdown(
            f"""
            <div class="hud-box">
                <div class="hud-icon">🎒</div>
                <div class="hud-number">
                    {len(adventure.get("inventory", []))}
                </div>
                <div class="hud-label">ITEMS</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # -----------------------------------------------------
    # LOCATION
    # -----------------------------------------------------

    st.markdown(
        "## 📍 "
        + str(
            adventure.get(
                "location",
                "Unknown"
            )
        )
    )

    st.write(
        adventure.get(
            "description",
            ""
        )
    )

    # -----------------------------------------------------
    # PREVIOUS EVENT
    # -----------------------------------------------------

    if st.session_state.adventure_event:

        clean_event, rewards = clean_event_text(
            st.session_state.adventure_event
        )

        st.markdown(
            "### 🎬 WHAT JUST HAPPENED"
        )

        if clean_event:

            st.write(clean_event)

        if rewards:

            st.write("")

            for reward in rewards:

                st.info(reward)

    # -----------------------------------------------------
    # KNOWLEDGE FACT
    # -----------------------------------------------------

    fact = adventure.get(
        "last_fact",
        ""
    )

    if fact:

        st.info(
            f"🧠 You discovered:\n\n{fact}"
        )

    # -----------------------------------------------------
    # INVENTORY
    # -----------------------------------------------------

    inventory = adventure.get(
        "inventory",
        []
    )

    if inventory:

        st.markdown("### 🎒 INVENTORY")

        st.write(
            " • ".join(inventory)
        )

    # -----------------------------------------------------
    # GAMEPLAY
    # -----------------------------------------------------

    if adventure.get("active", True):

        st.markdown("### 🎯 YOUR NEXT MOVE")

        st.markdown(
            "## Choose your action."
        )

        choices = adventure.get(
            "choices",
            []
        )

        if choices:

            option_columns = st.columns(
                min(len(choices), 3)
            )

            for i, choice in enumerate(
                choices[:3]
            ):

                with option_columns[i]:

                    if st.button(
                        str(choice),
                        key=f"adventure_choice_{i}",
                        use_container_width=True
                    ):

                        adventure_action(
                            choice
                        )

                        st.rerun()

        else:

            st.warning(
                "😵 The Adventure Master forgot the choices."
            )

    else:

        st.success(
            "🏁 ADVENTURE COMPLETE"
        )

        st.write(
            "Your adventure has ended. "
            "The world survived somehow."
        )

        if st.button(
            "🚀 START NEW ADVENTURE",
            use_container_width=True
        ):

            start_adventure()
            st.rerun()

    st.write("")

    n1, n2 = st.columns(2)

    with n1:

        if st.button(
            "🔄 NEW ADVENTURE",
            use_container_width=True
        ):

            start_adventure()
            st.rerun()

    with n2:

        if st.button(
            "🗺️ BACK TO MAP",
            use_container_width=True
        ):

            st.session_state.screen = "home"
            st.rerun()


# =========================================================
# SKILL VALLEY
# =========================================================

elif st.session_state.screen == "skill":

    monster = st.session_state.skill_monster

    st.markdown(
        '<div class="game-title">⚔️ SKILL VALLEY</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="game-subtitle">'
        f'{monster[0]} {monster[1]} is waiting.'
        '</div>',
        unsafe_allow_html=True
    )

    hp = st.session_state.skill_hp

    st.markdown(
        f"### ❤️ MONSTER HP: {hp}/100"
    )

    st.progress(
        hp / 100
    )

    st.write("")

    # -----------------------------------------------------
    # CREATE QUESTION
    # -----------------------------------------------------

    if st.session_state.skill_question is None:

        st.info(
            "🤖 The Quest Master is preparing your battle..."
        )

        try:

            question = get_question(
                st.session_state.level
            )

            if not isinstance(question, dict):

                st.error(
                    "Invalid question received."
                )

                st.stop()

            st.session_state.skill_question = question

            st.rerun()

        except Exception as e:

            st.error(
                "⚠️ Could not create battle."
            )

            st.code(str(e))

            st.stop()

    question = st.session_state.skill_question

    # -----------------------------------------------------
    # QUESTION
    # -----------------------------------------------------

    st.markdown(
        "### 🎯 YOUR CHALLENGE"
    )

    st.markdown(
        f"## {question.get('question', '')}"
    )

    # -----------------------------------------------------
    # OPTIONS
    # -----------------------------------------------------

    if not st.session_state.skill_answered:

        options = question.get(
            "options",
            []
        )

        option_columns = st.columns(2)

        for i, option in enumerate(options):

            with option_columns[i % 2]:

                if st.button(
                    f"⚔️ {option}",
                    key=f"skill_option_{i}",
                    use_container_width=True
                ):

                    answer_skill(option)

                    st.rerun()

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    else:

        if st.session_state.skill_correct:

            st.success(
                "💥 CRITICAL HIT!"
            )

            st.markdown(
                "## 👾 MONSTER DEFEATED!"
            )

        else:

            st.error(
                "🛡️ ATTACK BLOCKED!"
            )

        st.write(
            f"⭐ +{st.session_state.skill_reward} XP"
        )

        correct_answer = question.get(
            "answer"
        )

        if correct_answer:

            st.info(
                f"💡 Correct answer: {correct_answer}"
            )

        explanation = question.get(
            "explanation"
        )

        if explanation:

            st.write(explanation)

        st.write("")

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "⚔️ NEXT BATTLE",
                use_container_width=True
            ):

                start_skill()
                st.rerun()

        with c2:

            if st.button(
                "🗺️ MAP",
                use_container_width=True
            ):

                st.session_state.screen = "home"
                st.rerun()


# =========================================================
# CHARACTER
# =========================================================

elif st.session_state.screen == "character":

    st.markdown(
        '<div class="game-title">🧙 MY CHARACTER</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="game-subtitle">'
        f'{st.session_state.name}'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "👑 LEVEL",
            st.session_state.level
        )

    with c2:

        st.metric(
            "⭐ XP",
            st.session_state.xp
        )

    with c3:

        st.metric(
            "🪙 COINS",
            st.session_state.coins
        )

    st.write("")

    st.markdown("## 📊 CHARACTER SKILLS")

    st.write(
        f"🧠 Mind — {st.session_state.mind}/100"
    )

    st.progress(
        st.session_state.mind / 100
    )

    st.write(
        f"⚔️ Skill — {st.session_state.skill}/100"
    )

    st.progress(
        st.session_state.skill / 100
    )

    st.write(
        f"💪 Discipline — "
        f"{st.session_state.discipline}/100"
    )

    st.progress(
        st.session_state.discipline / 100
    )

    st.write(
        f"🎨 Creativity — "
        f"{st.session_state.creativity}/100"
    )

    st.progress(
        st.session_state.creativity / 100
    )

    st.write("")

    st.success(
        f"🏆 Adventures completed: "
        f"{st.session_state.completed}"
    )

    if st.button(
        "🗺️ BACK TO MAP",
        use_container_width=True
    ):

        st.session_state.screen = "home"
        st.rerun()