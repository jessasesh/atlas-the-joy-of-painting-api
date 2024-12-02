import csv
import re
import ast
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(BASE_DIR, "data")

# My attempt to extract and yes I need that many print statements
def extract_episodes():
    input_file = os.path.join(data_dir, "colors-used.txt")
    output_file = os.path.join(data_dir, "episodes.csv")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    data = []
    with open(input_file, "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            data.append({
                "Title": row["painting_title"],
                "Season": row["season"],
                "EpisodeNumber": row["episode"],
                "NumColors": row["num_colors"],
                "YouTubeLink": row["youtube_src"]
            })

    with open(output_file, "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["Title", "Season", "EpisodeNumber", "NumColors", "YouTubeLink"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Episodes data saved to {output_file}")

def extract_episode_colors():
    input_file = os.path.join(data_dir, "colors-used.txt")
    output_file = os.path.join(data_dir, "episode_colors.csv")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    data = []
    with open(input_file, "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            colors = ast.literal_eval(row["colors"])  # Convert string to list
            for color in colors:
                data.append({"Title": row["painting_title"], "Color": color.strip()})

    with open(output_file, "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["Title", "Color"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Episode colors data saved to {output_file}")


def extract_episode_subjects():
    input_file = os.path.join(data_dir, "subject-matter.txt")
    output_file = os.path.join(data_dir, "episode_subjects.csv")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    data = []
    with open(input_file, "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            title = row["TITLE"].strip('"')
            for key, value in row.items():
                if key not in {"EPISODE", "TITLE"} and value == "1":
                    data.append({"Title": title, "Subject": key})

    with open(output_file, "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["Title", "Subject"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Episode subjects data saved to {output_file}")


def extract_episode_dates():
    input_file = os.path.join(data_dir, "episode-dates.txt")
    output_file = os.path.join(data_dir, "episode_dates.csv")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    data = []
    with open(input_file, "r") as infile:
        for line in infile:
            match = re.match(r'"(.+)" \((.+)\)', line.strip())
            if match:
                title, date = match.groups()
                data.append({"Title": title.strip(), "Broadcast Date": date.strip()})

    with open(output_file, "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["Title", "Broadcast Date"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Episode dates saved to {output_file}")


if __name__ == "__main__":
    print("Starting extraction process...")
    extract_episodes()
    extract_episode_colors()
    extract_episode_subjects()
    extract_episode_dates()
    print("Extraction process complete. Cleaned files saved to the same directory as the input files.")
