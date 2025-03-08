import streamlit as st
from sentence_transformers import SentenceTransformer, util
import pandas as pd
from keybert import KeyBERT

bi_encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
corpus = []
contacts_df = pd.read_csv(
    "./data/department.csv",
    usecols=lambda x: x.lower() in ["department", "keywords"],
    encoding="latin-1",
)


def embed_contacts():
    global corpus
    corpus = []

    # Store each row to vector datastore
    for _, data in contacts_df.iterrows():
        # Use `|` as a delimiter
        row = f"{data['Department']}|{data['Keywords']}"
        corpus.append(row)
    # Embed list of rows into an in-memory vector store
    return bi_encoder.encode(corpus)


def query_vector(user_query: str) -> list[str]:
    hits = util.semantic_search(
        bi_encoder.encode([user_query]), embed_contacts(), top_k=5
    )[0]
    # Return department
    return [(f"{corpus[hit['corpus_id']].split('|')[0]}", hit["score"]) for hit in hits]


user_query = st.text_input("Enter FOIA description to get department")

if user_query:
    st.markdown("I think that this FOIA should be sent to: ")
    possible_departments = query_vector(user_query)

    st.markdown(
        f"**{possible_departments[0][0].strip()}** with a confidence of **{possible_departments[0][1] * 100:.2f}%**"
    )
    st.markdown("### But you could also try these departments:")

    for p in possible_departments[1:]:
        st.markdown(f"- {p[0]}")

    st.text("Did I get it right?")
    if st.button("Yes"):
        st.success("Yay 🥳")
    if st.button("No"):
        st.error("I'll get it next time 😢")
        form = st
        with st.form("foo"):
            selection = st.selectbox(
                "Which department does this query belong to?", contacts_df["Department"]
            )
            kw_model = KeyBERT()
            keywords = kw_model.extract_keywords(user_query)
            st.text(
                f"FOIA contains these keywords: {[x[0] for x in keywords]}. Add these keywords to the selected department?"
            )
            if st.form_submit_button("Yes"):
                curr_keywords = contacts_df[contacts_df[selection]][
                    "Keywords"
                ].str.split(",")
                st.text(f"Added {curr_keywords} to {selection}")
            else:
                st.text("👍")
