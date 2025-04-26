from bs4 import BeautifulSoup
import pandas as pd
import emoji
from urlextract import URLExtract
from datetime import datetime

def preprocess_telegram_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    messages = []
    usernames = []
    timestamps = []

    current_username = None

    for msg in soup.find_all("div", class_="message"):
        body = msg.find("div", class_="body")
        if not body:
            continue

        time_tag = body.find("div", class_="pull_right date details")
        user_tag = body.find("div", class_="from_name")
        text_tag = body.find("div", class_="text")

        # Ignore system messages that don’t have time
        if not time_tag:
            continue

        # Parse timestamp
        raw_time = time_tag.get("title")
        try:
            timestamp = datetime.strptime(raw_time.split(" UTC")[0], "%d.%m.%Y %H:%M:%S")
        except Exception:
            timestamp = pd.NaT

        # Update current username
        if user_tag:
            current_username = user_tag.text.strip()
        username = current_username if current_username else "Unknown"

        # Handle message text (even if it's a sticker or media caption)
        if text_tag:
            # Include text from nested tags (like <a>, <span>, <strong>)
            text = text_tag.get_text(separator=" ", strip=True)
        else:
            # If no text div is found, treat it as empty message
            text = "[Media or system message]"

        messages.append(text)
        usernames.append(username)
        timestamps.append(timestamp)

    # Create DataFrame
    df = pd.DataFrame({
        "username": usernames,
        "message": messages,
        "date": pd.to_datetime(timestamps, errors='coerce')
    })

    # Add derived time columns
    if pd.api.types.is_datetime64_any_dtype(df['date']):
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month_name()
        df["day"] = df["date"].dt.day_name()
        df["hour"] = df["date"].dt.hour
        df["minute"] = df["date"].dt.minute
    else:
        df["year"] = df["month"] = df["day"] = df["hour"] = df["minute"] = None

    # Word, URL, Emoji stats
    extractor = URLExtract()
    df["total_word"] = df["message"].apply(lambda x: len(str(x).split()))
    df["url_count"] = df["message"].apply(lambda x: len(extractor.find_urls(x)))
    df["emoji_count"] = df["message"].apply(lambda x: emoji.emoji_count(str(x)))

    df["period"] = df["hour"].apply(lambda x: (
        "Night" if pd.notnull(x) and 0 <= x < 6 else
        "Morning" if pd.notnull(x) and 6 <= x < 12 else
        "Afternoon" if pd.notnull(x) and 12 <= x < 18 else
        "Evening" if pd.notnull(x) else None
    ))

    return df
