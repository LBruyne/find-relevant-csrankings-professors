import re
import csv


# Remove all non-alphabetic characters from a string
def clean_text(text):
    return re.sub(r"[^a-zA-Z ]+", "", text).strip()


# Remove all non-numeric characters from a string
def clean_number(num_text):
    return re.sub(r"[^0-9]+", "", num_text).strip()


def save_universities_to_csv(filename, universities):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "University Rank",
                "University Name",
                "Professor Name",
                "Home Page",
                "Google Scholar",
            ]
        )

        for university in universities:
            for professor in university.get("professors", []):
                writer.writerow(
                    [
                        university.get("rank", ""),
                        university.get("name", ""),
                        professor.get("name", ""),
                        professor.get("home_page", ""),
                        professor.get("google_scholar", ""),
                    ]
                )


def load_universities_to_csv(filename, school_filter=None):
    prof_items = []

    with open(filename, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if school_filter and row["University Name"] not in school_filter:
                continue

            prof_items.append(
                {
                    "school": row["University Name"],
                    "name": row["Professor Name"],
                    "home_page": row["Home Page"],
                    "google_scholar": row["Google Scholar"],
                }
            )

    return prof_items


def save_relevant_professors_to_csv(filename, data):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "University Name",
                "Professor Name",
                "Home Page",
                "Google Scholar",
                "Overall Relevance",
                "Recent Relevant Highlights Count",
                "Recent Relevant Highlights",
            ]
        )

        for prof in data:
            writer.writerow(
                [
                    prof["school"],
                    prof["name"],
                    prof["home_page"],
                    prof["google_scholar"],
                    prof["relevance"],
                    prof["recent_highlights_num"],
                    prof["recent_highlights"],
                ]
            )
