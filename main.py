import csv
import re
import time
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from selenium import webdriver

def clean_text(text):
    return re.sub(r"[^a-zA-Z ]+", "", text).strip()

def clean_number(num_text):
    return re.sub(r"[^0-9]+", "", num_text).strip()

def print_field_choices():
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
        "Visualization": "visualization"
    }

    table = PrettyTable()
    table.field_names = ["Field", "Code"]

    for name, code in fields_dict.items():
        table.add_row([name, code])
    print(table)
        
def parse_professors(tbody):
    professors = []
    prof_trs = tbody.find_all('tr', recursive=False)
    for prof_tr in prof_trs:
        professor_info = parse_professor_info(prof_tr)
        if professor_info:
            professors.append(professor_info)
    return professors

def parse_professor_info(prof_tr):
    tds = prof_tr.find_all('td')
    if not tds:
        return None
    professor = {}
    for j, td in enumerate(tds):
        if j % 4 == 1:
            homepage = td.find('a', title="Click for author's home page.")
            if homepage:
                professor['name'] = clean_text(homepage.text)
                professor['home_page'] = homepage['href']
            google_scholar = td.find('a', title="Click for author's Google Scholar page.")
            if google_scholar:
                professor['google_scholar'] = google_scholar['href']
    return professor

def fetch_universities(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1) # Adjust this sleep time to avoid special situations according to your network speed.
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    universities = []
    table = soup.find('table', id='ranking')
    tbody = table.find('tbody')
    trs = tbody.find_all('tr', recursive=False)

    for i, tr in enumerate(trs):
        if i % 3 == 0:
            university_info = parse_university_info(tr)
        if i % 3 == 2 and university_info:
            university_info['professors'] = parse_professors(tr.find('tbody'))
            universities.append(university_info)

    return universities

def parse_university_info(tr):
    tds = tr.find_all('td')
    if not tds:
        return None
    university_info = {}
    for j, td in enumerate(tds):
        if j % 4 == 0:
            university_info['rank'] = clean_number(td.text)
        if j % 4 == 1:
            university_info['name'] = clean_text(td.text)
    return university_info

def save_to_csv(filename, universities):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['University Rank', 'University', 'Professor', 'Home Page', 'Google Scholar'])

        for university in universities:
            for professor in university.get('professors', []):
                writer.writerow([
                    university.get('rank', ''),
                    university.get('name', ''),
                    professor.get('name', ''),
                    professor.get('home_page', ''),
                    professor.get('google_scholar', '')
                ])

print_field_choices()
# fields_input = input("请输入您感兴趣的领域代码，用逗号分隔（例如 sec,crypt）: ")
# from_year = input("请输入开始年份（例如 2020）: ")
# to_year = input("请输入结束年份（例如 2024）: ")
fields_input = 'sec'
from_year = '2020'
to_year = '2024'

fields = fields_input.replace(",", "&")
url = f"https://csrankings.org/#/fromyear/{from_year}/toyear/{to_year}/index?{fields}&world"
print(f"Your URL: {url}")

universities = fetch_universities(url)
# print(universities)
filename = f'university-{from_year}-{to_year}-{fields_input.replace(",", "-")}.csv'
save_to_csv(filename, universities)
print(f"Data has been saved to {filename}")

