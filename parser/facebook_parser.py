import re
import pandas as pd
import emoji
from urlextract import URLExtract
from bs4 import BeautifulSoup

def preprocess_facebook(data):
    soup = BeautifulSoup(data, 'html.parser')
    messages = []
    usernames = []
    timestamps = []

    try:
        chat_blocks = soup.find_all('div', class_='_a6-g')

        for block in chat_blocks:
            user_tag = block.find('div', class_='_2ph_ _a6-h _a6-i')
            message_tag = block.find('div', class_='_2ph_ _a6-p')
            timestamp_tag = block.find('div', class_='_a72d')

            username = user_tag.get_text(strip=True) if user_tag else None
            timestamp = timestamp_tag.get_text(strip=True) if timestamp_tag else None

            # Check if message_tag exists
            if message_tag:
                try:
                    content_divs = message_tag.find_all('div')
                    message_text = ""
                    for div in content_divs:
                        text = div.get_text(strip=True)
                        if text and not text.lower().startswith("reacted"):
                            message_text = text
                            break
                except Exception as e:
                    message_text = ""  # If anything goes wrong, skip this message
            else:
                message_text = ""

            if username and message_text:
                messages.append(message_text)
                usernames.append(username)
                timestamps.append(timestamp)

    except Exception as e:
        print(f"Error during HTML parsing: {e}")

    # Convert to DataFrame
    df = pd.DataFrame({
        'username': usernames,
        'message': messages,
        'date': pd.to_datetime(timestamps, errors='coerce')
    })

    # Add time features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['time'] = df['date'].dt.strftime('%I:%M %p')

    # Word, emoji, URL count
    df['total_word'] = df['message'].apply(lambda x: len(str(x).split()))
    df['emoji_count'] = df['message'].apply(emoji.emoji_count)
    extractor = URLExtract()
    df['url_count'] = df['message'].apply(lambda x: len(extractor.find_urls(x)))

    # Period of Day
    df['period'] = df['hour'].apply(lambda x: (
        'Night' if 0 <= x < 6 else
        'Morning' if 6 <= x < 12 else
        'Afternoon' if 12 <= x < 18 else
        'Evening'))

    return df
