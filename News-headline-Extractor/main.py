import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Predefined news sites
NEWS_SITES = {
    "bbc": "https://www.bbc.com/news",
    "news18": "https://www.news18.com/",
    "cnn" : "https://edition.cnn.com/",
    "toi": "https://timesofindia.indiatimes.com"
}

def fetch_headlines(url, max_count=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/118.0.5993.90 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        headlines = []
        for tag in soup.find_all(["h1","h2", "h3"]):
            text = tag.get_text().strip()

            if text and text not in headlines:
                headlines.append(text)
                
            if len(headlines) >= max_count:
                break
        return headlines
    
    except requests.exceptions.RequestException as e:
        print("Error fetching the news website:", e)
        return []

def main():
    print(f"\n\n{"="*15} NEWS HEADLINE EXTRACTOR {"="*15}")
    while True :
        site_name = input("\n\nEnter news paper name ('q' for quit): ").strip().lower()
        if site_name.lower() == 'q':
            break

        if site_name in NEWS_SITES:
            url = NEWS_SITES[site_name]
        else:
            print("News site not available!!")
            url = input("\nPlease enter the website URL: ").strip()

        max_count_input = input("How many headlines do you want to see? : ").strip()
        max_count = int(max_count_input) if max_count_input.isdigit() else 10

        print(f"\nFetching latest headlines from {url}...\n")
        headlines = fetch_headlines(url, max_count=max_count)

        if not headlines:
            print("No headlines found. The website structure may be different or the site is unreachable.")
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"--- Latest News Headlines ({now}) ---\n")
            for i, headline in enumerate(headlines, start=1):
                print(f"{i}. {headline}")

if __name__ == "__main__":
    main()