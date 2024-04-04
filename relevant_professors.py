import time
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver

from utils import *
from config import *


def check_relevant_professors_in_scholar(items=[], keywords=[], max_count=10):
    relevant_professors = []
    count = 0
    driver = webdriver.Chrome()

    for prof_item in items:
        relevant_professor = {
            "school": prof_item.get("school", ""),
            "name": prof_item.get("name", ""),
            "home_page": prof_item.get("home_page", ""),
            "google_scholar": prof_item.get("google_scholar", ""),
        }

        prof_recent_highlights = []
        prof_relevance = 0
        scholar_url = prof_item.get("google_scholar", "")

        if scholar_url:

            # Sort by year
            scholar_year_url = scholar_url + "&view_op=list_works&sortby=pubdate"
            driver.get(scholar_year_url)
            time.sleep(
                SLEEP_TIME
            )  # Adjust this sleep time w.r.t. to your network speed.

            # Record recent highlights: recent works containing keywords
            soup = BeautifulSoup(driver.page_source, "html.parser")
            titles = soup.find_all("a", class_="gsc_a_at")
            for title in titles:
                for keyword in keywords:
                    if title.text.lower().count(keyword) > 0:
                        prof_recent_highlights.append(clean_text(title.text))
                        break

            # Sort by cite
            scholar_citation_url = scholar_url + "&view_op=list_works"
            driver.get(scholar_citation_url)
            time.sleep(
                SLEEP_TIME
            )  # Adjust this sleep time w.r.t. to your network speed.

            # Record domain relevance: works with high citation containing keywords
            soup = BeautifulSoup(driver.page_source, "html.parser")
            titles = soup.find_all("a", class_="gsc_a_at")
            prof_relevance = sum(
                title.text.lower().count(keyword)
                for title in titles
                for keyword in keywords
            )

        relevant_professor.update(
            {
                "recent_highlights_num": len(prof_recent_highlights),
                "recent_highlights": "[" + ", ".join(prof_recent_highlights) + "]",
                "relevance": prof_relevance,
            }
        )

        # Add this professor if he/she has recent highlights or relevance
        if (
            relevant_professor["recent_highlights_num"] > 0
            or relevant_professor["relevance"] > 0
        ):
            relevant_professors.append(relevant_professor)

        # Check maximum search count
        count += 1
        if count >= max_count:
            return relevant_professors

        # Adjust this time w.r.t. your network speed
        time.sleep(SLEEP_TIME)

    driver.quit()

    return relevant_professors


def parse_arguments(default_max_count):
    parser = argparse.ArgumentParser(
        description="Search for relevant professors based on keywords in paper titles."
    )
    parser.add_argument(
        "--filename",
        type=str,
        required=True,
        help="Datasource file, the output of csranking_top_professors.py (e.g., 2020-2024-sec.csv)",
    )
    parser.add_argument(
        "--keywords",
        type=str,
        required=True,
        help="Comma-separated list of relevant keywords in paper titles (e.g., \"adversarial, blockchain, LLM\")",
    )
    parser.add_argument(
        "--max_count",
        type=int,
        default=default_max_count,
        help="Maximum number of professors to search for (default: 50)",
    )
    parser.add_argument(
        "--schools",
        type=str,
        default="",
        help="Comma-separated list of university names to filter by (e.g., \"CISPA Helmholtz Center, Sanford University, Zhejiang University\")",
    )

    args = parser.parse_args()

    if args.max_count > default_max_count:
        args.max_count = default_max_count

    keywords = [keyword.strip().lower() for keyword in args.keywords.replace("\"", "").split(",")]
    school_filter = (
        [school.strip() for school in args.schools.replace("\"", "").split(",")]
        if args.schools
        else None
    )

    return args.filename, keywords, args.max_count, school_filter


if __name__ == "__main__":
    filename, keywords, max_count, school_filter = parse_arguments(DEFAULT_MAX_COUNT)

    # Read file
    print("Loading universities...")
    datasource = load_universities_to_csv(filename, school_filter=school_filter)

    print(f"Keywords: {keywords}")
    print("Start obtaining Google Scholar Info...")
    relevant_profs = check_relevant_professors_in_scholar(
        datasource, keywords, max_count=max_count
    )
    print("Finish obtaining Google Scholar Info...")

    # Sort according to the number of recent highlights
    relevant_profs_sorted = sorted(
        relevant_profs, key=lambda x: x["recent_highlights_num"], reverse=True
    )

    save_filename = "relevant-profs-" + "-".join(keywords) + ".csv"
    save_relevant_professors_to_csv(save_filename, relevant_profs_sorted)
    print(f"Relevant professors' information has been saved to {save_filename}")
