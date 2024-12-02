def filter_by_color(cursor, color):
    """
    Filter by color
    """
    query = """
        SELECT e.title, e.season, e.episode_number, c.color_name
        FROM Episodes e
        JOIN Episode_Color ec ON e.episode_id = ec.episode_id
        JOIN Colors c ON ec.color_id = c.color_id
        WHERE c.color_name = ?
    """
    cursor.execute(query, (color,))
    return [
        {"title": row[0], "season": row[1], "episode_number": row[2], "color": row[3]}
        for row in cursor.fetchall()
    ]


def filter_by_subject(cursor, subject):
    """
    Filter by subject
    """
    query = """
        SELECT e.title, e.season, e.episode_number, s.subject_name
        FROM Episodes e
        JOIN Episode_Subject es ON e.episode_id = es.episode_id
        JOIN Subjects s ON es.subject_id = s.subject_id
        WHERE s.subject_name = ?
    """
    cursor.execute(query, (subject,))
    return [
        {"title": row[0], "season": row[1], "episode_number": row[2], "subject": row[3]}
        for row in cursor.fetchall()
    ]
