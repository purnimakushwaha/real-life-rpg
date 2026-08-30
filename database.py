import sqlite3

DB_NAME = "real_life_rpg.db"


def get_connection():
    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,

            xp INTEGER DEFAULT 0,
            coins INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,

            mind INTEGER DEFAULT 0,
            discipline INTEGER DEFAULT 0,
            skill INTEGER DEFAULT 0,
            creativity INTEGER DEFAULT 0,

            completed INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,

            last_quest_date TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def create_player(name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO players (name)
        VALUES (?)
        """,
        (name,)
    )

    conn.commit()
    conn.close()


def get_player(name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            name,
            xp,
            coins,
            level,
            mind,
            discipline,
            skill,
            creativity,
            completed,
            streak,
            last_quest_date
        FROM players
        WHERE name = ?
        """,
        (name,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "name": row[0],
        "xp": row[1],
        "coins": row[2],
        "level": row[3],
        "mind": row[4],
        "discipline": row[5],
        "skill": row[6],
        "creativity": row[7],
        "completed": row[8],
        "streak": row[9],
        "last_quest_date": row[10]
    }


def save_player(data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE players
        SET
            xp = ?,
            coins = ?,
            level = ?,
            mind = ?,
            discipline = ?,
            skill = ?,
            creativity = ?,
            completed = ?,
            streak = ?,
            last_quest_date = ?
        WHERE name = ?
        """,
        (
            data["xp"],
            data["coins"],
            data["level"],
            data["mind"],
            data["discipline"],
            data["skill"],
            data["creativity"],
            data["completed"],
            data["streak"],
            data["last_quest_date"],
            data["name"]
        )
    )

    conn.commit()
    conn.close()