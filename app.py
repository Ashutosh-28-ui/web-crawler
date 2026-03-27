from flask import Flask, render_template, request
from scraper import crawl, data, image_links, visited, all_text, run_clustering, reset_data
import os
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    results = {}

    if request.method == "POST":
        url = request.form["url"]
        depth = int(request.form["depth"])

        
        reset_data()
        crawl(url, depth)

        clustering_result = run_clustering()

        if clustering_result:
            clusters, keywords = clustering_result
        else:
            clusters, keywords = None, None

        results = {
    "titles": data,
    "images": image_links,
    "clusters": clusters if clusters is not None else [],
    "keywords": keywords if keywords is not None else {}
}

    return render_template("index.html", results=results)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))