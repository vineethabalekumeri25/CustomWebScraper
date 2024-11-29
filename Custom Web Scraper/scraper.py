import requests
from bs4 import BeautifulSoup
import pandas as pd
from config import URL, OUTPUT_FILE


def scrape_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    # Send request to get the page content
    response = requests.get(URL, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve page: {URL} (Status Code: {response.status_code})")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    data = []

    # Find all recipe items (card)
    recipe_cards = soup.find_all('section', class_='comp mntl-three-post__inner mntl-universal-card-list mntl-document-card-list mntl-card-list mntl-block')

    for card in recipe_cards:
        # Title
        title = card.find('span', class_='card__title-text').text.strip() if card.find('span',
                class_='card__title-text') else 'No Title'
        # Link
        link = card.find('a', class_='mntl-card-list-items')['href'] if card.find('a',
                class_='mntl-card-list-items') else 'No Link'
        # Rating (number of stars)
        rating = card.find('div', class_='mm-recipes-card-meta__rating-count-number')
        rating = f"{rating.text.strip()}".replace("\n", " ") if rating else "No Rating"

        # Append data to list
        data.append({
            'Title': title,
            'Link': link,
            'Rating': rating
        })

    # If we have data, save it to a CSV file
    if data:
        df = pd.DataFrame(data)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Scraped data saved to {OUTPUT_FILE}")
    else:
        print("No data found.")


if __name__ == "__main__":
    scrape_data()