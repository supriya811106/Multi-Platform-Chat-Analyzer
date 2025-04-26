import streamlit as st
from parser.whatsapp_parser import preprocess_whatsapp
from parser.telegram_parser import preprocess_telegram_html
from parser.facebook_parser import preprocess_facebook
from utils import analysis

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import re
import random

st.set_page_config(page_title="Conversight 💬", page_icon="💬", layout="wide")
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

st.image("images/logo.png", use_column_width=True)
st.title("Your Chat Detective Sidekick 🕵️‍♂️💬")
st.caption("Where messages turn into memes, moods, and madness. 🎭📊")

st.markdown("""
🎉 **Hey Chat Sleuth!** Welcome to **Conversight** – your AI buddy for uncovering chat truths!  
Whether you're the group ghost 👻 or the non-stop talker 🎤, let's decode the drama together!
""")

st.markdown("### 🎯 Get Started in 4 Quirky Steps")
st.markdown("""
1️⃣ **Export** your chat from WhatsApp (TXT), Telegram, or Facebook (HTML).  
2️⃣ **Pick your platform** from the sidebar 🧭  
3️⃣ **Upload your chat file** — don't worry, we won’t judge 😄  
4️⃣ **Explore** secrets, moods, trends, and even emoji obsessions! 🤩
""")

# Sidebar Welcome Section
st.sidebar.markdown("## 💬 Welcome to Conversight!")
st.sidebar.markdown("""
Apni chats ka sach samajhne ka time aa gaya hai bro! 😂  
Bhai file upload kar, platform choose kar, aur chalu ho ja full analysis ke liye! 🔥  
Kya pata kaun sabse zyada active nikle ya kaun ghost bana baitha hai! 👻 
---
""")

st.sidebar.header("📂 Upload Your Chat File")
uploaded_file = st.sidebar.file_uploader("Drop it like it's hot 🔥 (.txt or .html)", type=["txt", "html"])
platform = st.sidebar.radio("Choose Your Chat Realm 🌍", ["WhatsApp", "Telegram", "Facebook"])

st.set_option('deprecation.showPyplotGlobalUse', False)

@st.cache_data(show_spinner=False, persist="disk")
def load_data(uploaded_file, platform):
    try:
        content = uploaded_file.read()

        if platform.lower() == "whatsapp":
            text = content.decode("utf-8")
            if not text.startswith("[") and not re.match(r"\d{1,2}/\d{1,2}/\d{2,4}", text):
                st.warning("⚠️ Hmm, this doesn't look like a WhatsApp TXT file. Did you export without media?")
                return None
            return preprocess_whatsapp(text)

        elif platform.lower() == "telegram":
            html = content.decode("utf-8")
            if "<div class=\"message default clearfix\"" not in html:
                st.warning("⚠️ Are you sure this is a Telegram file? We're not convinced 😅")
                return None
            return preprocess_telegram_html(html)

        elif platform.lower() == "facebook":
            html = content.decode("utf-8")
            if "_a6-g" not in html or "_a6-h" not in html:
                st.warning("⚠️ That doesn’t scream 'Facebook chat export'. Try another `.html` file from your archive.")
                return None
            return preprocess_facebook(html)

        return None

    except Exception as e:
        st.error(f"💥 Something broke while processing the file! Error: {e}")
        return None

fun_facts = [
    "💡 You blink 4x less while texting.",
    "📈 The average person sends 72 messages a day.",
    "🎨 Emojis were born in Japan in 1999!",
    "📊 Group chats are 34% more chaotic (don’t ask how we know).",
    "😮‍💨 1 out of every 5 texts contains an emoji. Probably more in your group."
]

fun_fact = random.choice(fun_facts)
st.info(f"🤔 Fun Fact: {fun_fact}")

if uploaded_file:
    df = load_data(uploaded_file, platform)

    if df is not None and not df.empty:
        user_list = df['username'].dropna().unique().tolist()
        user_list.sort()
        user_list.insert(0, "Overall Users")

        search_user = st.sidebar.text_input("🔍 Search a Chat Legend", "")
        filtered_users = [user for user in user_list if search_user.lower() in user.lower()]
        selected_user = st.sidebar.selectbox("🎭 Select a User", filtered_users)

        if selected_user == "Overall Users":
            analysis_menu = [
                "✨ Quick Chat Recap", "🏆 Who Talks Most?", "🎭 Mood Swings (Sentiment)",
                "🧠 Deep Talk Dive (NLP)", "🤜🤛 Showdown: Compare Users",
                "📅 Daily Habits Uncovered", "🔠 Words & Emojis Showdown"
            ]
        else:
            analysis_menu = [
                "✨ Quick Chat Recap", "🏆 Who Talks Most?", "🎭 Mood Swings (Sentiment)",
                "🧠 Deep Talk Dive (NLP)", "📅 Daily Habits Uncovered", "🔠 Words & Emojis Showdown"
            ]

        st.sidebar.header("🔧 Dive Into Data")
        choice = st.sidebar.selectbox("Choose Your Adventure", analysis_menu, index=0)

        if choice == "🤜🤛 Showdown: Compare Users":
            st.subheader("👥 Chat Duel: Who Rules the Chat?")
            users_to_compare = st.multiselect("Select contenders 👑", user_list)

            if len(users_to_compare) > 1:
                min_date = df["date"].min().date()
                max_date = df["date"].max().date()

                if min_date == max_date:
                    st.warning("📆 Only one date found. Time travel not supported (yet).")
                else:
                    selected_range = st.slider("⏳ Choose the Battle Timeline", min_date, max_date, (min_date, max_date))
                    if st.sidebar.button("🔥 Let the Battle Begin"):
                        users_activity = analysis.perform_comparative_analysis(
                            df, users_to_compare, selected_range[0], selected_range[1]
                        )
                        st.bar_chart(users_activity)
            else:
                st.warning("Please pick at least two warriors 👥")

        elif st.sidebar.button("Start Analysis 🚀"):
            if selected_user != 'Overall Users':
                df = df[df['username'] == selected_user]

            if choice == "✨ Quick Chat Recap":
                st.subheader("✨ Quick Chat Recap 📊")
                st.markdown(f"👑 Most Active: **{df['username'].value_counts().idxmax()}**")
                st.markdown(f"📆 Chattiest Day: **{df['day'].value_counts().idxmax()}**")
                st.markdown(f"⏰ Prime Talk Hour: **{df['hour'].value_counts().idxmax()}**")
                st.markdown(f"📏 Avg Words per Message: **{df['total_word'].mean():.2f}**")

                # STREAK FEATURE
                streak = analysis.longest_streak(df, selected_user if selected_user != "Overall Users" else None)
                st.markdown(f"🔥 **Longest Chat Streak:** {streak} day(s)")

                # THROWBACK FEATURE
                date, user, msg = analysis.throwback_message(df)
                st.markdown(f"🕰️ **First Message Ever:** *{msg}* by **{user}** on **{date}**")

                stats = analysis.fetch_stats(selected_user, df, platform)
                
                persona = analysis.personality_summary(stats)
                st.markdown(f"🧬 **Personality Match:** {persona}")

                comment = analysis.fun_summary_comment(stats)
                st.markdown(f"💬 **Conversight Says:** {comment}")

                st.download_button("📥 Grab CSV", df.to_csv(index=False), "chat_analysis.csv")

                with pd.ExcelWriter("chat_analysis_full.xlsx") as writer:
                    df.to_excel(writer, sheet_name="Messages", index=False)

                    emoji_df = analysis.emoji_helper(selected_user, df)
                    emoji_df.to_excel(writer, sheet_name="Emoji Summary", index=False)

                    tfidf_words = analysis.perform_tfidf_analysis(df["message"], platform)
                    pd.DataFrame(tfidf_words, columns=["Word", "TF-IDF Score"]).to_excel(writer, sheet_name="TF-IDF", index=False)

                    lda_topics = analysis.perform_lda_analysis(df["message"], 5, platform)
                    pd.DataFrame(lda_topics, columns=["LDA Topics"]).to_excel(writer, sheet_name="Topics", index=False)

                with open("chat_analysis_full.xlsx", "rb") as f:
                    st.download_button("📥 Download Full Report (Excel)", f, "chat_analysis_full.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                
                # Fun random reaction for this section
                st.warning(analysis.get_section_reaction("✨ Quick Chat Recap"))

            elif choice == "🏆 Who Talks Most?":
                stats = analysis.fetch_stats(selected_user, df, platform)
                titles = ["Messages 📩", "Words 📝", "Media 📷", "Links 🔗", "Emojis 😀", "Deleted 🗑️", "Edited ✍️", "Contacts 📞", "Locations 📍"]
                for title, value in zip(titles, stats):
                    st.markdown(f"### Total {title}:")
                    st.write(f"<div class='big-font'>{value}</div>", unsafe_allow_html=True)
                
                st.warning(analysis.get_section_reaction("🏆 Who Talks Most?"))

            elif choice == "🎭 Mood Swings (Sentiment)":
                df['Sentiment'] = df['message'].apply(analysis.extract_sentiment)
                st.subheader("Mood Map 📊")
                fig = px.bar(df['Sentiment'].value_counts(), labels={'index': 'Sentiment', 'value': 'Count'})
                st.plotly_chart(fig)

                st.subheader("Mood Over Time 🧠")
                sentiment_over_time = df.groupby(['date', 'Sentiment']).size().reset_index(name='Counts')
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.lineplot(data=sentiment_over_time, x='date', y='Counts', hue='Sentiment', ax=ax)
                st.pyplot(fig)

                vibe_summary = analysis.check_mood_vibe(df)
                st.success(f"🧠 Vibe Check: {vibe_summary}")

                st.warning(analysis.get_section_reaction("🎭 Mood Swings (Sentiment)"))

            elif choice == "🧠 Deep Talk Dive (NLP)":
                st.subheader("🧠 TF-IDF Keywords")
                top_words = analysis.perform_tfidf_analysis(df['message'], platform)
                st.write(top_words)

                st.subheader("💡 Topic Clusters (LDA)")
                topics = analysis.perform_lda_analysis(df['message'], 5, platform)
                for topic in topics:
                    st.write(topic)

                st.warning(analysis.get_section_reaction("🧠 Deep Talk Dive (NLP)"))

            elif choice == "📅 Daily Habits Uncovered":
                if selected_user == 'Overall Users':
                    top, bottom = analysis.most_least_busy_users(df)
                    st.subheader("🔥 Most Active Users")
                    st.bar_chart(top)
                    st.subheader("🧊 Least Active Users")
                    st.bar_chart(bottom)
                else:
                    st.subheader("🕓 Activity Over Time")
                    activity = analysis.user_activity_over_time(selected_user, df)
                    st.line_chart(activity)

                st.subheader("📅 Weekday Vibes")
                week = analysis.week_activity_map(selected_user, df)
                week.sort_index().plot(kind="bar")
                st.pyplot(plt.gcf())

                st.subheader("📆 Monthly Mojo")
                month = analysis.month_activity_map(selected_user, df)
                month.sort_index().plot(kind="bar")
                st.pyplot(plt.gcf())

                st.subheader("🔥 Emoji Burnmap")
                heatmap = analysis.activity_heatmap(selected_user, df)
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.heatmap(heatmap, cmap='coolwarm', annot=True, fmt=".0f", ax=ax)
                st.pyplot(fig)

                st.warning(analysis.get_section_reaction("📅 Daily Habits Uncovered"))

            elif choice == "🔠 Words & Emojis Showdown":
                st.subheader("📚 Most Common Words")
                wc_array = analysis.create_wordcloud(selected_user, df, platform)
                st.image(wc_array)

                st.subheader("😆 Top Emojis Used")
                emoji_df = analysis.emoji_helper(selected_user, df)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.dataframe(emoji_df.head(5))

                if not emoji_df.empty:
                    st.subheader("📊 Emoji Vibes Pie Chart")
                    fig, ax = plt.subplots()
                    ax.pie(emoji_df['Frequency'].head(), labels=emoji_df['Emoji'].head(), autopct='%1.1f%%')
                    st.pyplot(fig)

                    guess = analysis.guess_top_emoji(emoji_df)
                    st.info(guess)
                
                st.warning(analysis.get_section_reaction("🔠 Words & Emojis Showdown"))

st.sidebar.markdown("---")
st.sidebar.header("💬 Was this fun?")
was_helpful = st.sidebar.selectbox("Rate your vibe with Conversight 💖", ["Please choose", "Loved it!", "It was cool", "Needs more sparkle"])
if was_helpful != "Please choose":
    feedback = st.sidebar.text_area("Drop your thoughts or memes here...")
    if st.sidebar.button("✨ Submit Vibe"):
        st.sidebar.success("You're awesome! Thanks for the feedback 💌")

st.sidebar.markdown("---")
st.sidebar.markdown("🧠 Built with 💻 by Supriya · © 2025 Conversight")