import requests
from bs4 import BeautifulSoup
import time

def clean_amazon_url(url):
    if "/dp/" in url:
        asin = url.split("/dp/")[1].split("/")[0]
        return f"https://www.amazon.in/dp/{asin}"
    return url


def fetch_amazon_html(url):
    url = clean_amazon_url(url)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-IN,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
    }

    response = requests.get(url, headers=headers, timeout=30)

    if response.status_code != 200:
        raise Exception("Failed to fetch Amazon page")

    return response.text


def detect_availability(soup):

    # Check official availability block first
    availability_div = soup.find("div", id="availability")
    if availability_div:
        text = availability_div.get_text(" ", strip=True).lower()

        if "currently unavailable" in text:
            return "Currently Unavailable ❌"

        if "in stock" in text:
            return "In Stock ✅"

    # Fallback: keyword scan 
    body_text = soup.get_text(" ", strip=True).lower()

    unavailable_patterns = [
        "currently unavailable",
        "we don't know when or if this item will be back",
        "not available for delivery",
    ]

    for p in unavailable_patterns:
        if p in body_text:
            return "Currently Unavailable ❌"

    in_stock_patterns = [
        "in stock",
        "only left in stock",
        "available for delivery",
        "order now"
    ]

    for p in in_stock_patterns:
        if p in body_text:
            return "In Stock ✅"

    return "Availability Unknown ⚠️"


def parse_product(html):
    soup = BeautifulSoup(html, "html.parser")

    name = soup.find("span", id="productTitle")
    price = soup.find("span", class_="a-price-whole")

    availability = detect_availability(soup)

    return {
        "name": name.get_text(strip=True) if name else "Not Found",
        "price": price.get_text(strip=True) if price else "Price Not Available",
        "availability": availability
    }

def get_amazon_product(url):
    html = fetch_amazon_html(url)
    return parse_product(html)

def main():
    print("=== Amazon Product Availability Checker ===")

    while True:
        url = input("\nEnter Amazon Product URL (or exit): ").strip()
        if url.lower() == "exit":
            break

        try:
            html = fetch_amazon_html(url)
            data = parse_product(html)

            print("\n📦 Product Details")
            print("----------------------")
            print("Name        :", data["name"])
            print("Price       :", data["price"])
            print("Availability:", data["availability"])

            time.sleep(2)

        except Exception as e:
            print("❌ Error:", e)


if __name__ == "__main__":
    main()
