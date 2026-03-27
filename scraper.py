import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

all_text = []
data = {}
image_links = []
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

        # ✅ Extract text AFTER soup is created
        text = soup.get_text(separator=" ", strip=True)
        all_text.append(text)

        # Title
        title = soup.title.string.strip() if soup.title and soup.title.string else "No title"
        print("Title:", title)
        data[url] = title

        # Links
        links = soup.find_all('a')

        for link in links[:10]:
            href = link.get('href')

            if href:
                full_url = urljoin(url, href)

                if "#" in full_url:
                    full_url = full_url.split("#")[0]

                crawl(full_url, depth - 1)

        # Images
        images = soup.find_all('img')

        for img in images[:5]:
            src = img.get('src')

            if src:
                full_img = urljoin(url, src)
                print("Image:", full_img)
                image_links.append(full_img)

    except Exception as e:
        print("Error:", e)


# 🔽 INPUT
start_url = input("Enter start URL: ")
depth = int(input("Enter depth (1-3 recommended): "))

crawl(start_url, depth)

# 🔽 SAVE FILES
with open("crawled_links.txt", "w", encoding="utf-8") as f:
    for link in visited:
        f.write(link + "\n")

with open("crawled_data.txt", "w", encoding="utf-8") as f:
    for link, title in data.items():
        f.write(f"{title} -> {link}\n")

with open("images.txt", "w", encoding="utf-8") as f:
    for img in image_links:
        f.write(img + "\n")

print("\nFiles saved successfully!")


vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X = vectorizer.fit_transform(all_text)

kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)
terms = vectorizer.get_feature_names_out()

for i in range(3):
    print(f"\nCluster {i} top words:")
    center = kmeans.cluster_centers_[i]
    top_indices = center.argsort()[-10:][::-1]

    for index in top_indices:
        print(terms[index])

print("\nCluster assignments:")
print(kmeans.labels_)