import os
import sqlite3


db_folder = os.path.join(os.path.dirname(__file__), "db")
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "episodes.db")

schema = """
CREATE TABLE IF NOT EXISTS Episodes (
    episode_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    season INTEGER NOT NULL,
    episode_number INTEGER NOT NULL,
    broadcast_date DATE
);

CREATE TABLE IF NOT EXISTS Subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Colors (
    color_id INTEGER PRIMARY KEY AUTOINCREMENT,
    color_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Episode_Subject (
    episode_id INTEGER,
    subject_id INTEGER,
    FOREIGN KEY (episode_id) REFERENCES Episodes(episode_id),
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
);

CREATE TABLE IF NOT EXISTS Episode_Color (
    episode_id INTEGER,
    color_id INTEGER,
    FOREIGN KEY (episode_id) REFERENCES Episodes(episode_id),
    FOREIGN KEY (color_id) REFERENCES Colors(color_id)
);
"""

def initialize_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript(schema)
    conn.commit()
    conn.close()

    print(f"Database initialized and tables created at {db_path}")

def verify_tables():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()

    print("Tables in db:")
    for table in tables:
        print(table[0])

if __name__ == "__main__":
    initialize_database()
    verify_tables()
