from playwright.sync_api import sync_playwright, TimeoutError
from bs4 import BeautifulSoup
import time


def clean_amazon_url(url):
    if "/dp/" in url:
        asin = url.split("/dp/")[1].split("/")[0]
        return f"https://www.amazon.in/dp/{asin}"
    return url


def fetch_amazon_html(url):
    url = clean_amazon_url(url)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="en-IN"
        )

        page = context.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector("#productTitle", timeout=15000)
        except TimeoutError:
            print("⚠️ Page loaded but product title not detected yet.")

        time.sleep(3)  # let JS settle
        html = page.content()

        browser.close()
        return html


def parse_product(html):
    soup = BeautifulSoup(html, "html.parser")

    name = soup.find("span", id="productTitle")
    price = soup.find("span", class_="a-price-whole")
    availability = soup.find("div", id="availability")

    return {
        "name": name.get_text(strip=True) if name else "Not Found",
        "price": price.get_text(strip=True) if price else "Price Not Available",
        "availability": availability.get_text(strip=True) if availability else "Availability Not Found"
    }

def get_amazon_product(url):
    html = fetch_amazon_html(url)
    return parse_product(html)

def main():
    while True:
        url = input("\nEnter Amazon Product URL (or exit): ").strip()
        if url.lower() == "exit":
            break

        html = fetch_amazon_html(url)
        data = parse_product(html)

        print("\n📦 Product Details")
        print("----------------------")
        print("Name        :", data["name"])
        print("Price       :", data["price"])
        print("Availability:", data["availability"])


if __name__ == "__main__":
    main()
