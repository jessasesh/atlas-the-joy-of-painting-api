from flask import Blueprint, request, jsonify
import sqlite3
import os

api_bp = Blueprint("api", __name__)

#DB Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "db", "episodes.db")


#Filter Episodes
@api_bp.route("/episodes/filter", methods=["GET"])
def filter_episodes():
    color = request.args.get("color", "").strip()
    subject = request.args.get("subject", "").strip()
    season = request.args.get("season", "").strip()

    query = "SELECT e.title, e.season, e.episode_number, e.broadcast_date FROM Episodes e"
    filters = []
    params = []

    if color:
        query += " JOIN Episode_Color ec ON e.episode_id = ec.episode_id JOIN Colors c ON ec.color_id = c.color_id"
        filters.append("c.color_name = ?")
        params.append(color)

    if subject:
        query += " JOIN Episode_Subject es ON e.episode_id = es.episode_id JOIN Subjects s ON es.subject_id = s.subject_id"
        filters.append("s.subject_name = ?")
        params.append(subject)

    if season:
        filters.append("e.season = ?")
        params.append(season)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY e.season, e.episode_number"

    #Fetch Data
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        #JSON Response
        episodes = [
            {
                "title": row[0],
                "season": row[1],
                "episode_number": row[2],
                "broadcast_date": row[3],
            }
            for row in rows
        ]
        return jsonify(episodes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
