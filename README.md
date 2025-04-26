# 📊 Chat Analyzer

A Python-based chat analysis tool to extract insights from **WhatsApp**, **Facebook Messenger**, and **Telegram** conversations.  
It includes cleaning, statistics generation, personality summarization, sentiment analysis, TF-IDF, LDA topic modeling, and fun comparisons!

---

## ✨ Features

- **Clean messages**: Remove noise like media placeholders, deleted/edited markers, and usernames.
- **Basic Stats**: Total messages, words, media, links, emojis, deleted messages, and more.
- **Personality Summary**: Based on emoji use, message length, media sharing, and deletion frequency.
- **Longest Chat Streak**: Find out the longest messaging streak by user.
- **Throwback Message**: Display the oldest message in the chat.
- **Fun Summary Comments**: Automatically generates quirky chat comments.
- **Sentiment Analysis**: Positive, Neutral, or Negative vibe classification.
- **Mood Vibe Check**: Overall mood based on sentiment distribution.
- **TF-IDF Analysis**: Identify important words across chats.
- **LDA Topic Modeling**: Extract discussion topics from the chat.
- **Comparative Analysis**: Compare message counts between selected users over a time period.
- **Activity Insights**: Find the most and least active users.

---

## 🛠 Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/supriya811106/Multi-Platform-Chat-Anayzer.git
    cd Multi-Platform-Chat-Anayzer
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

    **Required libraries:**
    - pandas
    - numpy
    - emoji
    - textblob
    - wordcloud
    - scikit-learn

---

## 🚀 Usage

```python
import chat_analyzer  # Assuming you save the above code as chat_analyzer.py

# Clean messages
cleaned_messages = chat_analyzer.clean_messages(messages, platform="telegram", usernames=["John", "Jane"])

# Fetch stats
stats = chat_analyzer.fetch_stats(selected_user="John", df=your_dataframe, platform="telegram")

# Generate personality summary
summary = chat_analyzer.personality_summary(stats)

# Sentiment extraction
df["Sentiment"] = df["message"].apply(chat_analyzer.extract_sentiment)

# Perform TF-IDF
important_words = chat_analyzer.perform_tfidf_analysis(messages)

# Perform LDA topic modeling
topics = chat_analyzer.perform_lda_analysis(messages)

# Comparative analysis
comparison = chat_analyzer.perform_comparative_analysis(df, users_to_compare=["John", "Jane"], start_date="2024-01-01", end_date="2024-04-01")
```

---

## 📈 Output Examples

- **Personality Summaries** like:
  - 🎉 Emoji Queen/King
  - 🧠 Philosopher
  - 📸 Storyteller
- **Fun Comments** like:
  - 🧨 You’re breaking records with that message count!
  - 🤣 Emoji addict detected.
- **Sentiment Mood** like:
  - 😄 Lots of good vibes here!
  - 😬 More negative vibes than good ones!

---

## 📝 Notes

- Platform-specific cleaning is supported: WhatsApp, Facebook Messenger, and Telegram.
- Can work on both individual and group chats.
- Optimized for conversational datasets with `username`, `message`, `date`, `day` columns.

---


