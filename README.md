# 📊 Chat Analyzer

**Conversight** is a Python-based chat analysis tool to extract insights from **WhatsApp**, **Facebook Messenger**, and **Telegram** conversations.  
It includes cleaning, statistics generation, personality summarization, sentiment analysis, TF-IDF, LDA topic modeling, and fun comparisons!

---

## 🚀 Features

1. **Cross-Platform Support:**
   - **WhatsApp**: Import and analyze exported `.txt` files from WhatsApp.
   - **Telegram**: Import and analyze exported `.html` files from Telegram.
   - **Facebook**: Import and analyze exported `.html` files from Facebook.

2. **Chat Summary:**
   - Get an **overall chat recap**, including:
     - Most Active User 🗣️
     - Chattiest Day 📅
     - Prime Talk Hour 🕒
     - Average Words per Message 📏
   - **Streak Feature**: View your longest uninterrupted streak of chat activity.
   - **Throwback Feature**: Discover the first-ever message in your chat history.

3. **User Comparison:**
   - **Chat Duel**: Compare two or more users' activity.
   - Metrics include messages, words, media, emojis, sentiment, and more.

4. **Sentiment Analysis:**
   - **Mood Map**: Visualize the overall sentiment of your messages.
   - **Mood Over Time**: Track mood changes throughout the chat timeline.
   - Sentiment scores and vibes are automatically assigned to each message.

5. **Deep Talk Dive (NLP Analysis):**
   - **TF-IDF Keywords**: Find the most important keywords in the chat.
   - **Topic Clustering (LDA)**: Discover hidden topics through Latent Dirichlet Allocation (LDA).

6. **User Activity:**
   - **Most Active and Least Active Users**: View daily and monthly activity heatmaps.
   - **Weekday and Monthly Activity**: Track user engagement across different timeframes.

7. **Words & Emojis Showdown:**
   - **Word Cloud**: Visualize the most commonly used words in the chat.
   - **Top Emojis Used**: View the most frequently used emojis with a frequency breakdown.
   - **Emoji Pie Chart**: A pie chart displaying the distribution of emojis used.

8. **Export Data:**
   - **Download CSV and Excel Reports**: Export detailed chat and emoji analysis for further inspection.
   - **Full Report**: Download a comprehensive chat analysis with all metrics, sentiment, word analysis, and emoji usage.

9. **Fun Facts & Interactive Elements:**
   - **Chat Fun Facts**: Enjoy random fun facts about texting and chat behavior.
   - **Engagement Reactions**: Get quirky reactions from Conversight based on your data.

---

## 🎯 How to Use

1. **Export** your chat from WhatsApp (TXT), Telegram (HTML), or Facebook (HTML).
2. **Pick Your Platform** from the sidebar.
3. **Upload Your Chat File**.
4. **Explore** various features such as user comparison, sentiment analysis, emoji showdown, and more!

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


