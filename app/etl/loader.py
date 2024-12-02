import os
import csv
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../db/episodes.db")
data_dir = os.path.join(BASE_DIR, "data")

# Load episodes data
def load_episodes():
    input_file = os.path.join(data_dir, "episodes.csv")
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(input_file, "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            cursor.execute("""
                INSERT INTO Episodes (title, season, episode_number, broadcast_date)
                VALUES (?, ?, ?, ?);
            """, (row["Title"], row["Season"], row["EpisodeNumber"], row.get("Broadcast Date")))

    conn.commit()
    conn.close()
    print(f"Episodes data loaded into the database from {input_file}")

# Load subjects data
def load_subjects():
    relationships_file = os.path.join(data_dir, "episode_subjects.csv")

    if not os.path.exists(relationships_file):
        raise FileNotFoundError("Episode-subjects file not found.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Load relationships
    with open(relationships_file, "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            cursor.execute("""
                INSERT INTO Episode_Subject (episode_id, subject_id)
                SELECT e.episode_id, s.subject_id
                FROM Episodes e, Subjects s
                WHERE e.title = ? AND s.subject_name = ?;
            """, (row["Title"], row["Subject"]))

    conn.commit()
    conn.close()

# Load colors data
def load_colors():
    input_file = os.path.join(data_dir, "episode_colors.csv")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Load colors
    with open(input_file, "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            cursor.execute("""
                INSERT INTO Episode_Color (episode_id, color_id)
                SELECT e.episode_id, c.color_id
                FROM Episodes e, Colors c
                WHERE e.title = ? AND c.color_name = ?;
            """, (row["Title"], row["Color"]))

    conn.commit()
    conn.close()

def cleanup_duplicates():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Episodes
        SET title = TRIM(REPLACE(REPLACE(LOWER(title), '  ', ' '), '\"', ''));
    """)


    cursor.execute("""
        UPDATE Episodes
        SET title = UPPER(SUBSTR(title, 1, 1)) || LOWER(SUBSTR(title, 2))
        WHERE title LIKE '% %';
    """)

    cursor.execute("SELECT DISTINCT title FROM Episodes")
    for row in cursor.fetchall():
        print(row[0])

    cursor.execute("""
        DELETE FROM Episodes
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM Episodes
            GROUP BY title, season, episode_number, broadcast_date
        );
    """)

    cursor.execute("SELECT * FROM Episodes")
    for row in cursor.fetchall():
        print(row)

    cursor.execute("""
        DELETE FROM Episode_Subject
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM Episode_Subject
            GROUP BY episode_id, subject_id
        );
    """)


    cursor.execute("""
        DELETE FROM Episode_Color
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM Episode_Color
            GROUP BY episode_id, color_id
        );
    """)

    conn.commit()
    conn.close()



if __name__ == "__main__":
    print("Starting data loading process...")
    load_episodes()
    load_subjects()
    load_colors()
    cleanup_duplicates()
    print("Data loading process complete.")
