import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

data = {}
visited = set()

def crawl(url, depth):
    if depth == 0 or url in visited:
        return

    print(f"\nCrawling: {url}")
    visited.add(url)

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string.strip() if soup.title and soup.title.string else "No title"
        print("Title:", title)

        data[url] = title

        links = soup.find_all('a')

        for link in links[:10]:
            href = link.get('href')

            if href:
                full_url = urljoin(url, href)

                if "#" in full_url:
                    full_url = full_url.split("#")[0]

                crawl(full_url, depth - 1)

    except Exception as e:
        print("Error:", e)


start_url = input("Enter start URL: ")
depth = int(input("Enter depth (1-3 recommended): "))

crawl(start_url, depth)

with open("crawled_links.txt", "w", encoding="utf-8") as f:
    for link in visited:
        f.write(link + "\n")

print("\nSaved all crawled links to crawled_links.txt")

with open("crawled_data.txt", "w", encoding="utf-8") as f:
    for link, title in data.items():
        f.write(f"{title} -> {link}\n")

print("Saved all crawled data to crawled_data.txt")