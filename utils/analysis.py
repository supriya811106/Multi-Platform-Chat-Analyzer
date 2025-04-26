import re
import emoji
import pandas as pd
import random
from textblob import TextBlob
from wordcloud import WordCloud
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter

stop_words_list = ['deleted', 'null', 'omitted', 'message', 'media', 'photo', 'video', 'sticker', 'animation', 'voice message', 'file']

# -------------------------------
# Clean Messages
# -------------------------------
def clean_messages(messages, platform="generic", usernames=None):
    if platform == "facebook":
        exclude_patterns = ['unsent a message', 'edited a message', 'media']
    elif platform == "telegram":
        exclude_patterns = ['photo', 'video', 'sticker', 'animation', 'voice message', 'file', 'audio', 'location']
    else:
        exclude_patterns = ['<Media omitted>', 'This message was deleted', '<This message was edited>']

    messages = messages[~messages.str.lower().str.contains('|'.join(exclude_patterns), na=False)]

    if usernames is not None:
        pattern = r'\b(?:' + '|'.join(re.escape(name.lower()) for name in usernames) + r')\b'
        messages = messages.apply(lambda x: re.sub(pattern, '', x.lower()))
    else:
        messages = messages.str.lower()

    return messages

# -------------------------------
# --- Personality Summary ---
# -------------------------------
def personality_summary(stats):
    messages, words, media, links, emojis, deleted, edited, contacts, locations = stats
    if emojis > messages * 0.3:
        return "🎉 Emoji Queen/King"
    elif words / max(messages, 1) > 15:
        return "🧠 Philosopher"
    elif deleted > 50:
        return "🕵️‍♂️ The Mysterious One"
    elif media > messages * 0.5:
        return "📸 Storyteller (via memes)"
    else:
        return "😎 Chill Conversationalist"

# -------------------------------
# --- Longest Chat Streak ---
# -------------------------------
def longest_streak(df, user=None):
    if user:
        df = df[df['username'] == user]
    df = df.sort_values(by="date")
    df['day_diff'] = df['date'].diff().dt.days.fillna(0).astype(int)
    streaks = (df['day_diff'] != 1).cumsum()
    max_streak = df.groupby(streaks).size().max()
    return max_streak

# -------------------------------
# --- Throwback Message ---
# -------------------------------
def throwback_message(df):
    oldest = df.sort_values(by='date').iloc[0]
    return oldest['date'].strftime('%d %b %Y'), oldest['username'], oldest['message']

# -------------------------------
# Basic Stats
# -------------------------------
def fetch_stats(selected_user, df, platform="generic"):
    try:
        if selected_user != 'Overall Users':
            df = df[df['username'] == selected_user]

        total_messages = df.shape[0]
        total_word_count = df['total_word'].sum()

        if platform == "facebook":
            media_keywords = ['image', 'video', 'sticker', 'file', 'attachment']
        elif platform == "telegram":
            media_keywords = ['photo', 'video', 'sticker', 'file', 'voice message', 'animation', 'audio']
        else:
            media_keywords = ['<Media omitted>']

        total_media_messages = df['message'].str.lower().str.contains('|'.join(media_keywords), na=False).sum()
        total_url_count = df['url_count'].sum()
        total_emoji_count = df['emoji_count'].sum()

        if platform == "facebook":
            deleted_message = df[df['message'].str.contains("unsent a message", case=False, na=False)]
            edited_messages = df[df['message'].str.contains("edited a message", case=False, na=False)]
        elif platform == "telegram":
            deleted_message = df[df['message'].str.contains("This message was deleted", case=False, na=False)]
            edited_messages = pd.DataFrame()
        else:
            deleted_message = df[df['message'].str.contains("This message was deleted", case=False, na=False)]
            edited_messages = df[df['message'].str.contains("<This message was edited>", case=False, na=False)]

        phone_pattern = r'\+?\d{2,4}[\s-]?\d{10}'
        shared_contacts = df[df['message'].str.contains(phone_pattern, case=False, na=False) |
                             df['message'].str.contains('.vcf', case=False, na=False)]['message']

        location_pattern = r'//maps\.google\.com/\?q=\d+\.\d+,\d+\.\d+'
        shared_locations = df[df['message'].str.contains(location_pattern, case=False, na=False)]['message']

        return (
            total_messages, total_word_count, total_media_messages, total_url_count,
            total_emoji_count, len(deleted_message), len(edited_messages),
            len(shared_contacts), len(shared_locations)
        )

    except Exception as e:
        print(f"Error in fetching stats: {e}")
        return 0, 0, 0, 0, 0, 0, 0, 0, 0

# -------------------------------
# Fun Summary Comments
# -------------------------------
def fun_summary_comment(stats):
    messages, words, media, links, emojis, deleted, edited, contacts, locations = stats
    comments = []

    if messages > 10000:
        comments.append("🧨 You’re breaking records with that message count!")
    elif messages > 5000:
        comments.append("📬 Message overload alert!")
    else:
        comments.append("💌 A calm and cozy chat... for now.")

    if emojis > 3000:
        comments.append("🤣 Emoji addict detected.")
    elif emojis > 1000:
        comments.append("😎 Nice emoji game!")

    if deleted > 100:
        comments.append("🤐 Someone’s got secrets... lots of deleted messages.")

    if media > 1000:
        comments.append("🎥 Chat full of media drama!")

    if words / max(messages, 1) < 3:
        comments.append("🤫 Short and sweet chats!")

    return " ".join(comments)

# -------------------------------
# Sentiment Analysis
# -------------------------------
def extract_sentiment(message):
    try:
        analysis = TextBlob(message)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return 'neutral'

def check_mood_vibe(df):
    try:
        sentiment_counts = df['Sentiment'].value_counts()
        if sentiment_counts.get('negative', 0) > sentiment_counts.get('positive', 0):
            return "😬 More negative vibes than good ones! Need a hug?"
        elif sentiment_counts.get('positive', 0) > sentiment_counts.get('negative', 0):
            return "😄 Lots of good vibes here! Keep it up!"
        else:
            return "😐 Balanced moods all around."
    except:
        return ""

# -------------------------------
# TF-IDF
# -------------------------------
def perform_tfidf_analysis(messages, platform="generic", usernames=None):
    try:
        messages = clean_messages(messages, platform, usernames)
        vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
        tfidf = vectorizer.fit_transform(messages)
        words = vectorizer.get_feature_names_out()
        word_scores = np.array(tfidf.sum(axis=0)).flatten()
        filtered_words = [(words[i], word_scores[i]) for i in np.argsort(word_scores)[::-1]
                          if words[i] not in stop_words_list]
        return filtered_words[:5]
    except Exception as e:
        print(f"Error in TF-IDF analysis: {e}")
        return []

# -------------------------------
# LDA Topic Modeling
# -------------------------------
def perform_lda_analysis(messages, num_topics=5, platform="generic", usernames=None):
    try:
        messages = clean_messages(messages, platform, usernames)
        vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
        bow = vectorizer.fit_transform(messages)
        words = vectorizer.get_feature_names_out()
        lda = LatentDirichletAllocation(n_components=num_topics, random_state=0)
        lda.fit(bow)

        topic_words = []
        for i, topic in enumerate(lda.components_):
            top_words_array = topic.argsort()[-5:][::-1]
            topic_list = [words[j] for j in top_words_array if words[j] not in stop_words_list]
            topic_words.append(f"Topic {i + 1}: {' | '.join(topic_list)}")
        return topic_words
    except Exception as e:
        print(f"Error in LDA analysis: {e}")
        return []

# -------------------------------
# Comparative Analysis
# -------------------------------
def perform_comparative_analysis(df, users_to_compare, start_date, end_date):
    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date) + pd.Timedelta(days=1)
        filtered_df = df[(df["date"] >= start_date) & (df["date"] < end_date)]
        user_filtered_df = filtered_df[filtered_df["username"].isin(users_to_compare)]
        return user_filtered_df["username"].value_counts()
    except Exception as e:
        print(f"Error in comparative analysis: {e}")
        return pd.Series()

# -------------------------------
# Activity Insights
# -------------------------------
def most_least_busy_users(df):
    try:
        counts = df['username'].value_counts()
        return counts.head(5), counts.tail(5)
    except Exception as e:
        print(f"Error in busy users analysis: {e}")
        return pd.Series(), pd.Series()

def user_activity_over_time(selected_user, df):
    try:
        if selected_user != 'Overall Users':
            df = df[df['username'] == selected_user]
        return df.groupby(['date', 'username'])['message'].count().unstack().fillna(0)
    except Exception as e:
        print(f"Error in user activity over time: {e}")
        return pd.DataFrame()

def week_activity_map(selected_user, df):
    try:
        if selected_user != 'Overall Users':
            df = df[df['username'] == selected_user]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return df['day'].value_counts().reindex(days).fillna(0)
    except Exception as e:
        print(f"Error in weekly activity map: {e}")
        return pd.Series()

def month_activity_map(selected_user, df):
    try:
        if selected_user != 'Overall Users':
            df = df[df['username'] == selected_user]
        return df['month'].value_counts()
    except Exception as e:
        print(f"Error in monthly activity map: {e}")
        return pd.Series()

def activity_heatmap(selected_user, df):
    try:
        if selected_user != 'Overall Users':
            df = df[df['username'] == selected_user]
        return df.groupby(['day', 'period']).size().unstack().fillna(0)
    except Exception as e:
        print(f"Error in activity heatmap: {e}")
        return pd.DataFrame()

# -------------------------------
# WordCloud
# -------------------------------
def create_wordcloud(selected_user, df, platform="generic", stopwords_path='stop_hinglish.txt'):
    try:
        with open(stopwords_path, 'r') as f:
            stop_words = set(f.read().split())

        if selected_user != 'Overall Users':
            df = df[df['username'] == selected_user]

        if platform == "facebook":
            exclude_patterns = ['unsent a message', 'edited a message', 'media']
        elif platform == "telegram":
            exclude_patterns = ['photo', 'video', 'sticker', 'voice message', 'file', 'animation']
        else:
            exclude_patterns = ['<Media omitted>', 'This message was deleted', '<This message was edited>']

        df = df[~df['message'].str.lower().str.contains('|'.join(exclude_patterns), na=False)]

        wc = WordCloud(width=800, height=400, min_font_size=10, background_color='white', stopwords=stop_words)
        df_wc = wc.generate(' '.join(df['message']))
        return df_wc.to_image()
    except Exception as e:
        print(f"Error in word cloud generation: {e}")
        return None

# -------------------------------
# Emoji Analysis
# -------------------------------
def emoji_helper(selected_user, df):
    try:
        if selected_user != 'Overall Users':
            df = df[df['username'] == selected_user]

        all_possible_emojis = set(emoji.EMOJI_DATA.keys())
        all_emojis = []

        for message in df['message']:
            all_emojis.extend([ch for ch in str(message) if ch in all_possible_emojis])

        emoji_df = pd.DataFrame(Counter(all_emojis).most_common(), columns=['Emoji', 'Frequency'])
        return emoji_df
    except Exception as e:
        print(f"Error in emoji analysis: {e}")
        return pd.DataFrame()

def guess_top_emoji(emoji_df):
    try:
        if not emoji_df.empty:
            return f"🤔 Wanna guess the top emoji? It's... **{emoji_df.iloc[0]['Emoji']}** used **{emoji_df.iloc[0]['Frequency']}** times!"
        return "❓ No emojis? What kind of chat is this?!"
    except Exception as e:
        print(f"Error guessing top emoji: {e}")
        return "🤷‍♂️ Couldn't analyze top emoji."
    
# -------------------------------
# Fun Reactions based on the choice
# -------------------------------
def get_section_reaction(choice):
    if choice == "✨ Quick Chat Recap":
        return random.choice([
            "💬 Looks like you’ve been busy chatting! 📈",
            "📅 Who knew recapping chats could be this fun?",
            "🧐 The chat detective in you is shining!",
            "📊 Every word counts in this conversation!",
        ])
    
    elif choice == "🏆 Who Talks Most?":
        return random.choice([
            "🎤 Talker of the year! You sure love to chat.",
            "🗣️ You’re the life of the chat group! Keep talking!",
            "📈 More words than a novelist! 😲",
            "🔥 Looks like you're the conversation champion!",
        ])
    
    elif choice == "🎭 Mood Swings (Sentiment)":
        return random.choice([
            "😆 Lots of highs and lows in these messages!",
            "😢 Whoa, did someone get emotional here?",
            "🧠 Mood alert: this chat has some serious mood swings!",
            "📊 Your feelings are all over the map!",
        ])
    
    elif choice == "🧠 Deep Talk Dive (NLP)":
        return random.choice([
            "🔍 Let’s dig deeper — this chat has layers!",
            "💡 Looks like you’ve been diving into some deep topics!",
            "🧠 Conversations here are a deep dive into the unknown.",
            "🎓 These messages have PhD-level insights!",
        ])
    
    elif choice == "🤜🤛 Showdown: Compare Users":
        return random.choice([
            "👑 Who’s the real chat king? Let’s find out!",
            "⚔️ The battle of words has begun!",
            "🎭 May the best talker win!",
            "👥 Who dominates the chat? Time to compare!",
        ])
    
    elif choice == "📅 Daily Habits Uncovered":
        return random.choice([
            "🕓 Every day’s a busy day for you!",
            "📅 You’ve got some serious daily habits!",
            "🔥 Time to uncover those secret activity patterns!",
            "📊 A daily routine in chat? Let’s analyze that!",
        ])
    
    elif choice == "🔠 Words & Emojis Showdown":
        return random.choice([
            "📚 These words are flying faster than your emoji game!",
            "😂 Emojis and words: the ultimate combo!",
            "🔠 This chat has its own dictionary of words and emojis!",
            "📊 Let’s see who’s the true emoji master here!",
        ])
    
    else:
        return "💬 Keep chatting and let’s see what else you uncover!"
    