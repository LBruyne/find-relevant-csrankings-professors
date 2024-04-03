import csv
import re
import time
import requests
from bs4 import BeautifulSoup

def load_from_csv(filename):
    universities = []

    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        current_university = {}
        for row in reader:
            if not current_university or current_university['name'] != row['University Name']:
                if current_university:
                    universities.append(current_university)
                current_university = {'name': row['University'], 'rank': row['University Rank'], 'professors': []}

            professor = {
                'name': row['Professor'],
                'home_page': row['Home Page'],
                'google_scholar': row['Google Scholar']
            }
            current_university['professors'].append(professor)
        
        if current_university:
            universities.append(current_university)

    return universities

def check_keywords_in_scholar(universities, keywords):
    for university in universities:
        for professor in university.get('professors', []):
            if(professor.get('name', '') != 'Michael Backes'): 
                continue
            scholar_url = professor.get('google_scholar', '')
            print(scholar_url)
            if scholar_url:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
                page = requests.get(scholar_url, headers=headers)
                print(page)
                soup = BeautifulSoup(page.text, 'html.parser')
                titles = soup.find_all('div', class_='gsc_a_at')
                keyword_count = sum(title.text.lower().count(keyword) for title in titles for keyword in keywords)
                print(keyword_count)
            time.sleep(1)

# keyword_input = input("请输入关键词，用逗号分隔（例如: cryptography, blockchain）: ")
# keywords = [keyword.strip().lower() for keyword in keyword_input.split(',')] 
keywords = ['adversarial', 'snark']

print('Start obtaining Google Scholar Info...')

filename = 'university.csv'
universities = load_from_csv(filename)
print(universities)

check_keywords_in_scholar(universities, keywords)
