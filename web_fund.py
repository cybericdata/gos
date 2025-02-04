import requests
from bs4 import BeautifulSoup
import csv
import time

url = 'https://womenfund.org/news'
BASE_URL = 'https://womenfund.org/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

response = requests.get(url, headers=headers)

print(response)
if response.status_code != 200:
    print (" Failed to retrieve data:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, 'html.parser')


time.sleep(5) 
raw_data = []
for item in soup.find_all('article'):
    span_tag = item
    link = item.find('a')

    if span_tag:
        title = span_tag.get_text(strip=True)
        href = link['href']

        newsResponse = requests.get(href, headers=headers)
        newsSoup = BeautifulSoup(newsResponse.text, 'html.parser')
        time.sleep(3)
        
        news_array = []
        for news_data in newsSoup.find_all('p'):
            news = news_data.get_text(strip=True)
            news_array.append(news)

        raw_data.append({
            'title': title,
            'news': news_array
        })

    else:
        print("No span found")

with open('gender_equality_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'news'])
    writer.writeheader()
    writer.writerows(raw_data)

for data in raw_data:
    print(f" Title: {data['title']}, news: {data['news']}")