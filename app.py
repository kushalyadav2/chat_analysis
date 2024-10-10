import streamlit as st
import seaborn as sns
from matplotlib import pyplot as plt

import helper
import preprocessor

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Chose the file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique users
    user_list = df['users'].unique().tolist()
    # if 'group_notification' in user_list:
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'over all')

    selected_user = st.sidebar.selectbox("Show analysis wrt ", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media")
            st.title(num_media_messages)

        with col4:
            st.header("Total Link")
            st.title(num_links)

        # Monthly timeline
        st.title("Monthly Timeline")
        monthly_timeline = helper.month_timeline(selected_user, df)  # Ensure the function name is also updated
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline['time'], monthly_timeline['messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")

        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            week_activity_map = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(week_activity_map.index, week_activity_map.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            month_activity_map = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(month_activity_map.index, month_activity_map.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, ax=ax)
        st.pyplot(fig)

        # Find the busiest user

        if selected_user == 'over all':
            st.title('Most Busy user')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # word cloud

        st.title('Word Cloud')
        df_wc = helper.creates_word(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most common words
        most_common_df = helper.most_common_words(selected_user, df)
        # st.dataframe(most_common_df)
        fig, ax = plt.subplots()
        ax.bar(most_common_df['Word'], most_common_df['Count'], color='red')
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)


        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title('Emoji Analysis')
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
