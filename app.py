import streamlit as st
import json
import numpy as np
from topics import topics

answer_options = topics

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
        topic_1 = st.selectbox("Topic-1", answer_options)
        topic_2 = st.selectbox("Topic-2", answer_options)
        topic_3 = st.selectbox("Topic-3", answer_options)
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            with open("scores_per_topics.json", "r") as f:
                counts = json.load(f)
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
            sorted_keys = sorted(counts, key=counts.get)
            st.error("One of the topics with highest re-identification we found is:\t"+np.random.choice(sorted_keys[-5:]))
            st.success("One of the topics with lowest re-identification we found is:\t"+np.random.choice(sorted_keys[:5]))

if __name__ == "__main__":
    main()
