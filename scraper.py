import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Global storage
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
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text
        text = soup.get_text(separator=" ", strip=True)
        all_text.append(text)

        # Title
        title = soup.title.string.strip() if soup.title and soup.title.string else "No title"
        print("Title:", title)
        data[url] = title

        # Links (limit for speed)
        links = soup.find_all('a')

        for link in links[:3]:  # keep small for speed
            href = link.get('href')

            if href:
                full_url = urljoin(url, href)

                if "#" in full_url:
                    full_url = full_url.split("#")[0]

                crawl(full_url, depth - 1)

        
        images = soup.find_all('img')

        for img in images[:5]:
            src = img.get('src')

            if src:
                full_img = urljoin(url, src)
                print("Image:", full_img)
                image_links.append(full_img)

    except Exception as e:
        print("Error:", e)



def run_clustering():
    if len(all_text) < 2:
        print("Not enough data for clustering")
        return None

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans

    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(all_text)

    num_clusters = min(3, len(all_text))

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X)

    print("\nCluster assignments:")
    print(kmeans.labels_)

   
    terms = vectorizer.get_feature_names_out()

    cluster_keywords = {}

    for i in range(num_clusters):
        center = kmeans.cluster_centers_[i]
        top_indices = center.argsort()[-5:][::-1]

        words = [terms[index] for index in top_indices]
        cluster_keywords[i] = words

    return kmeans.labels_, cluster_keywords



def reset_data():
    all_text.clear()
    data.clear()
    image_links.clear()
    visited.clear()