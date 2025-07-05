import requests
from bs4 import BeautifulSoup

def scrape(url, tag, class_name=None):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    if class_name:
        elements = soup.find_all(tag, class_=class_name)
    else:
        elements = soup.find_all(tag)

    results = [el.get_text(strip=True) for el in elements]
    return results

if __name__ == "__main__":
    # 🔗 Example: Scrape article titles from Python's official blog
    url = "https://blog.python.org/"
    tag = "h3"
    class_name = "post-title"

    titles = scrape(url, tag, class_name)
    for i, title in enumerate(titles, 1):
        print(f"{i}. {title}")
