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
