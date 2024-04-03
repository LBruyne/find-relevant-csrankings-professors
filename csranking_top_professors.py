import csv
import time
import argparse
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from selenium import webdriver

from config import *
from utils import *

fields_dict = {
    "Artificial intelligence": "ai",
    "Computer vision": "vision",
    "Machine learning & data mining": "mlmining",
    "Natural language processing": "nlp",
    "The Web & information retrieval": "ir",
    "Computer architecture": "arch",
    "Computer networks": "comm",
    "Computer security": "sec",
    "Databases": "mod",
    "Design automation": "da",
    "Embedded & real-time systems": "bed",
    "High-performance computing": "hpc",
    "Mobile computing": "mobile",
    "Measurement & perf. analysis": "metrics",
    "Operating systems": "ops",
    "Programming languages": "plan",
    "Software engineering": "soft",
    "Algorithms & complexity": "act",
    "Cryptography": "crypt",
    "Logic & verification": "log",
    "Comp. bio & bioinformatics": "bio",
    "Computer graphics": "graph",
    "Computer science education": "csed",
    "Economics & computation": "ecom",
    "Human-computer interaction": "chi",
    "Robotics": "robotics",
    "Visualization": "visualization",
}


def print_field_choices():
    table = PrettyTable()
    table.field_names = ["Field", "Code"]

    for name, code in fields_dict.items():
        table.add_row([name, code])
    print(table)


def parse_professors(tbody):
    professors = []
    prof_trs = tbody.find_all("tr", recursive=False)
    # Professors' info are stored in another tr list
    for prof_tr in prof_trs:
        professor_info = parse_professor_info(prof_tr)
        if professor_info:
            professors.append(professor_info)
    return professors


def parse_professor_info(prof_tr):
    tds = prof_tr.find_all("td")
    if not tds:
        return None
    professor = {}
    for j, td in enumerate(tds):
        if j % 4 == 1:
            homepage = td.find("a", title="Click for author's home page.")
            if homepage:
                professor["name"] = clean_text(homepage.text)
                professor["home_page"] = homepage["href"]
            google_scholar = td.find(
                "a", title="Click for author's Google Scholar page."
            )
            if google_scholar:
                professor["google_scholar"] = google_scholar["href"]
    return professor


def fetch_universities(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(
        WAIT_TIME
    )  # Adjust this sleep time to avoid special situations according to your network speed.
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    universities = []
    table = soup.find("table", id="ranking")
    tbody = table.find("tbody")
    trs = tbody.find_all("tr", recursive=False)

    for i, tr in enumerate(trs):
        if i % 3 == 0:
            # Parse university info
            university_info = parse_university_info(tr)
        if i % 3 == 2 and university_info:
            # Parse professors
            university_info["professors"] = parse_professors(tr.find("tbody"))
            universities.append(university_info)

    return universities


def parse_university_info(tr):
    tds = tr.find_all("td")
    if not tds:
        return None
    university_info = {}
    for j, td in enumerate(tds):
        if j % 4 == 0:
            university_info["rank"] = clean_number(td.text)
        if j % 4 == 1:
            university_info["name"] = clean_text(td.text)
    return university_info


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Fetch universities and professors data from CSRankings."
    )
    parser.add_argument(
        "--fields",
        type=str,
        required=True,
        help='Code of relevant fields, using "," to split multiple fields (e.g., "sec,ai" for Security and Artificial Intelligence)',
    )
    parser.add_argument(
        "--start_year", type=int, default=2020, help="Start year (default 2020)"
    )
    parser.add_argument(
        "--end_year", type=int, default=time.localtime().tm_year, help="End year (default 2024)"
    )

    args = parser.parse_args()

    if args.start_year > args.end_year or args.end_year > time.localtime().tm_year:
        parser.error("Invalid year range.")

    if not all(field in set(fields_dict.values()) for field in args.fields.split(",")):
        parser.error("Invalid field code.")

    return (
        args.fields.replace(" ", "").replace(",", "&"),
        args.start_year,
        args.end_year,
    )


if __name__ == "__main__":
    print_field_choices()
    fields, from_year, to_year = parse_arguments()

    url = f"https://csrankings.org/#/fromyear/{from_year}/toyear/{to_year}/index?{fields}&world"
    print(f"Your URL: {url}")

    universities = fetch_universities(url)
    # print(universities)
    filename = f'{from_year}-{to_year}-{fields.replace(" ", "").replace("&", "-")}.csv'
    save_universities_to_csv(filename, universities)
    print(f"Data has been saved to {filename}")
