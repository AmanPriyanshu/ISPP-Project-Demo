import streamlit as st
import json
import numpy as np
from topics import topics

answer_options = topics

with open("scores_per_topics.json", "r") as f:
    counts = json.load(f)

sorted_keys = sorted(counts, key=counts.get)

def main():
    st.title("Umasking Threats! Topics API")

    with st.sidebar:
        st.image('topics_logo.png')
        st.markdown("""
**Google's Topics API** is a new advertising mechanism that replaces third-party cookies. It has been rolled out to the majority of Chrome-browser users. It assigns broad interest categories to users based on their browsing history, allowing advertisers to show relevant ads without tracking individual websites they visit. _It claims to be a "Privacy-Preserving" mechanism for advertisements!_

However, we verify on these claims through **re-identification** and **membership-inference attacks!** 
            """)

    with st.form("my_form"):
        with st.expander("**Select 3 Topics**", expanded=True):
            question_1 = """
Select three topics either:

(a) Synonymous to your Phone's Topics which you can find at: \"[chrome://topics-internals/](chrome://topics-internals/)\"
or
(b) Select three topics which interest you the most!
            """
            st.markdown(question_1)

            # Use st.selectbox for user selection
            selected_topics = st.session_state.get("selected_topics", [])
            selected_topics.append(st.selectbox("Topic-1", answer_options, key="topic_1",  index=answer_options.index(np.random.choice(sorted_keys[-np.random.randint(1,150):]))))
            selected_topics.append(st.selectbox("Topic-2", answer_options, key="topic_2", index=answer_options.index(np.random.choice(sorted_keys[-np.random.randint(1,len(sorted_keys)):]))))
            selected_topics.append(st.selectbox("Topic-3", answer_options, key="topic_3", index=answer_options.index(np.random.choice(sorted_keys[:]))))
            st.session_state.selected_topics = selected_topics[-3:]

        submitted = st.form_submit_button("Submit")
        if submitted:
            # Retrieve selected topics from session_state
            topic_1, topic_2, topic_3 = st.session_state.selected_topics
            # st.info(f"You selected:\n```\nTopic 1: {topic_1}\nTopic 2: {topic_2}\nTopic 3: {topic_3}\n```")

            c_1 = counts.get(topic_1, 0)
            c_2 = counts.get(topic_2, 0)
            c_3 = counts.get(topic_3, 0)
            score = np.mean([c_1, c_2, c_3])
            st.write("Your re-identification score is: "+str(round(100*score, 2))+"%")
            if score<0.3:
                st.success("You have a re-identification chance of less than 30%. Therefore, you are **likely not to be re-identified** based on the dataset we experimented with!")
            elif score<0.5:
                st.info("You have a re-identification chance of less than 50% but above 30%. Therefore, you **can be re-identified, but there's a lower chance of it** based on the dataset we experimented with.")
            elif score<0.75:
                st.warning("You have a re-identification chance of less than 75% but above 50%. Therefore, you **can be re-identified, and there's a higher chance you will be** based on the dataset we experimented with.")
            else:
                st.error("You have a re-identification chance of more than 75%. Therefore, you are **likely to be re-identified** based on the dataset we experimented with.")

            st.write("**FUN FACT!!**")
            sorted_keys_fun_fact = sorted(counts, key=counts.get)  # Use a different variable name
            st.error("One of the topics with the highest re-identification we found is:\t"+np.random.choice(sorted_keys_fun_fact[-5:]))
            st.success("One of the topics with the lowest re-identification we found is:\t"+np.random.choice(sorted_keys_fun_fact[:5]))

    st.markdown("**Team:** Aman Priyanshu, Yash Maurya, Suriya Ganesh, and Vy Tran")
    st.markdown("**Under Supervision of:** Prof. Hana Habib and Prof. Norman Sadeh  & TA Saranya Vijayakumar")

if __name__ == "__main__":
    main()
