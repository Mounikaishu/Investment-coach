import sqlite3
import hashlib
from datetime import datetime, timedelta

DB_NAME = "users.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            amount REAL,
            type TEXT,
            category TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saving_streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            last_saving_date TEXT,
            total_xp INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            badge_name TEXT,
            earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(username, badge_name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            topic TEXT,
            score INTEGER,
            total INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# ── Auth ──────────────────────────────────────────────

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users VALUES (NULL, ?, ?)",
                       (username, hash_password(password)))
        # Initialize streak record for new user
        cursor.execute(
            "INSERT OR IGNORE INTO saving_streaks (username) VALUES (?)",
            (username,)
        )
        conn.commit()
        conn.close()
        return True
    except:
        return False

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# ── Transactions ──────────────────────────────────────

def add_transaction(username, amount, t_type, category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (username, amount, type, category)
        VALUES (?, ?, ?, ?)
    """, (username, amount, t_type, category))
    conn.commit()
    conn.close()
    # Update streak if it's a saving/income entry
    if t_type == "Income" or category == "Investment":
        update_streak(username)

def get_transactions(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT amount, type, category, date
        FROM transactions
        WHERE username=?
        ORDER BY date DESC
    """, (username,))
    data = cursor.fetchall()
    conn.close()
    return [tuple(row) for row in data]

def get_recent_transactions(username, limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT amount, type, category, date
        FROM transactions
        WHERE username=?
        ORDER BY date DESC
        LIMIT ?
    """, (username, limit))
    data = cursor.fetchall()
    conn.close()
    return [tuple(row) for row in data]

# ── Saving Streaks ────────────────────────────────────

def update_streak(username):
    conn = get_connection()
    cursor = conn.cursor()

    # Ensure streak record exists
    cursor.execute(
        "INSERT OR IGNORE INTO saving_streaks (username) VALUES (?)",
        (username,)
    )

    cursor.execute(
        "SELECT current_streak, longest_streak, last_saving_date FROM saving_streaks WHERE username=?",
        (username,)
    )
    row = cursor.fetchone()
    today = datetime.now().strftime("%Y-%m-%d")

    if row:
        current_streak = row["current_streak"]
        longest_streak = row["longest_streak"]
        last_date = row["last_saving_date"]

        if last_date == today:
            # Already logged today — no change
            conn.close()
            return current_streak

        if last_date:
            last = datetime.strptime(last_date, "%Y-%m-%d")
            diff = (datetime.now() - last).days
            if diff == 1:
                current_streak += 1
            elif diff > 1:
                current_streak = 1
        else:
            current_streak = 1

        longest_streak = max(longest_streak, current_streak)
    else:
        current_streak = 1
        longest_streak = 1

    # Award XP for saving: 10 XP base + streak bonus
    xp_earned = 10 + (current_streak * 2)

    cursor.execute("""
        UPDATE saving_streaks
        SET current_streak=?, longest_streak=?, last_saving_date=?,
            total_xp = total_xp + ?
        WHERE username=?
    """, (current_streak, longest_streak, today, xp_earned, username))

    conn.commit()
    conn.close()
    return current_streak

def get_streak(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT current_streak, longest_streak, last_saving_date, total_xp FROM saving_streaks WHERE username=?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "current_streak": row["current_streak"],
            "longest_streak": row["longest_streak"],
            "last_saving_date": row["last_saving_date"],
            "total_xp": row["total_xp"]
        }
    return {"current_streak": 0, "longest_streak": 0, "last_saving_date": None, "total_xp": 0}

# ── Badges ────────────────────────────────────────────

def award_badge(username, badge_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO badges (username, badge_name) VALUES (?, ?)",
            (username, badge_name)
        )
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_badges(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT badge_name, earned_date FROM badges WHERE username=? ORDER BY earned_date DESC",
        (username,)
    )
    data = cursor.fetchall()
    conn.close()
    return [{"name": row["badge_name"], "date": row["earned_date"]} for row in data]

# ── Quiz Scores ───────────────────────────────────────

def save_quiz_score(username, topic, score, total):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quiz_scores (username, topic, score, total)
        VALUES (?, ?, ?, ?)
    """, (username, topic, score, total))
    conn.commit()
    conn.close()
    # Award XP for quiz completion
    add_xp(username, 15 + score * 5)

def get_quiz_scores(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT topic, score, total, date
        FROM quiz_scores
        WHERE username=?
        ORDER BY date DESC
    """, (username,))
    data = cursor.fetchall()
    conn.close()
    return [dict(row) for row in data]

# ── XP Helpers ────────────────────────────────────────

def add_xp(username, xp_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO saving_streaks (username) VALUES (?)",
        (username,)
    )
    cursor.execute(
        "UPDATE saving_streaks SET total_xp = total_xp + ? WHERE username=?",
        (xp_amount, username)
    )
    conn.commit()
    conn.close()

def get_total_savings(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COALESCE(SUM(amount),0) FROM transactions WHERE username=? AND type='Income'",
        (username,)
    )
    income = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COALESCE(SUM(amount),0) FROM transactions WHERE username=? AND type='Expense'",
        (username,)
    )
    expense = cursor.fetchone()[0]
    conn.close()
    return income - expense
