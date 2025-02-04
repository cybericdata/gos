# identify the specific areas education, health, violence against women e.t.c
# what data types are needed
# compile list of data sources like website, databases and online platforms

# https://womenaffairs.gov.ng/ https://womenfund.org/ https://www.womenconsortiumofnigeria.org/ https://www.gpinigeria.org/ 
# https://www.wrapanigeria.org/ https://witin.org/ https://womeningh.org/ 


import requests
from bs4 import BeautifulSoup
import csv
import time

def fetch_and_parse(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data from {url}: {e}")
        return None

def extract_data(soup, base_url):
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
        else:
            print("No span or link found")
    return data

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'news'])
        writer.writeheader()
        writer.writerows(data)

def main():
    url = 'https://womenaffairs.gov.ng/index.php/publications-2'
    base_url = 'https://womenaffairs.gov.ng/'
    output_file = 'gender_equality_web_data_1.csv'

    soup = fetch_and_parse(url)
    if soup:
        data = extract_data(soup, base_url)
        save_to_csv(data, output_file)

if __name__ == "__main__":
    main()