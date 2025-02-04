import time
from web_affairs import fetch_and_parse, save_to_csv
import os
from dotenv import load_dotenv

load_dotenv()

def extract_data(soup):
    print("Extracting data...")
    time.sleep(5) 
    raw_data = []
    for item in soup.find_all('article'):
        span_tag = item
        link = item.find('a')

        if span_tag:
            title = span_tag.get_text(strip=True)
            href = link['href']

            newsSoup = fetch_and_parse(href)
            time.sleep(2)
            
            news_array = []
            for news_data in newsSoup.find_all('p'):
                news = news_data.get_text(strip=True)
                news_array.append(news)

            raw_data.append({
                'title': title,
                'news': news_array
            })
            print("Done Extracting news data")
        else:
            print("No span found")
    return raw_data


def main():
    url = os.getenv("WEB_TWO_URL")
    output_file = 'data/gender_equality_web_data_2.csv'

    soup = fetch_and_parse(url)
    if soup:
        data = extract_data(soup)
        save_to_csv(data, output_file)

if __name__ == "__main__":
    main()

# for data in raw_data:
#     print(f" Title: {data['title']}, news: {data['news']}")