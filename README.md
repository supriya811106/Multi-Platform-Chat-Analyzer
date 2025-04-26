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
- streamlit: For creating the web interface of the chat analyzer.
- pandas: For data manipulation and analysis.
- matplotlib: For plotting data visualizations.
- seaborn: For enhanced data visualizations.
- plotly: For interactive visualizations.
- textblob: For performing sentiment analysis.
- wordcloud: For generating word clouds.
- numpy: For numerical operations.
- scikit-learn: For machine learning tools like CountVectorizer and LatentDirichletAllocation.
- urlextract: For extracting URLs from chat messages.
- emoji: For processing emoji data in messages.
- beautifulsoup4: For parsing HTML data, used for Telegram chat parsing.
- datetime: For handling date and time data.

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


