# identify the specific areas education, health, violence against women e.t.c
# what data types are needed
# compile list of data sources like website, databases and online platforms

import requests
from bs4 import BeautifulSoup
import csv
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_and_parse(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("Site connection established..")
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data from {url}: {e}")
        return None

def extract_data(soup, base_url):
    print("Extracting data...")
    data = []
    for item in soup.find_all('li'):
        span_tag = item
        link = item.find('a')

        if span_tag and link:
            strong_tag = span_tag.find('strong')
            if strong_tag:
                title = strong_tag.get_text(strip=True)
                href = link['href']
                news_url = base_url + href

                news_soup = fetch_and_parse(news_url)
                if news_soup:
                    news = news_soup.find('div').get_text(strip=True)
                    data.append({
                        'title': title,
                        'news': news
                    })
                    print("Done Extracting news data") 
        else:
            print("No span or link found")
    return data

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'news'])
        writer.writeheader()
        writer.writerows(data)

def main():
    url = os.getenv("WEB_ONE_URL")
    base_url = os.getenv("WEB_ONE_BASE_URL")
    output_file = 'data/gender_equality_web_data_1.csv'

    soup = fetch_and_parse(url)
    if soup:
        data = extract_data(soup, base_url)
        print(data)
        save_to_csv(data, output_file)

if __name__ == "__main__":
    main()