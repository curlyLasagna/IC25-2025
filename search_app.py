import streamlit as st
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import pandas as pd

bi_encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
corpus = []


def embed_contacts():
    global corpus
    corpus = []
    contacts_df = pd.read_csv(
        "./data/department.csv",
        usecols=lambda x: x.lower() in ["name", "department", "keywords"],
        encoding="latin-1",
    )

    # Store each row to vector datastore
    for _, data in contacts_df.iterrows():
        # Use `/` as a delimiter
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
    st.markdown("I think that this query should be sent to: ")
    possible_departments = query_vector(user_query)

    for dep, score in possible_departments:
        st.text(f"{dep} ranks {cross_encoder.predict([dep, user_query])}")

    st.text(
        f"{possible_departments[0][0]} with a confidence of {possible_departments[0][1] * 100:.2f}% "
    )
    st.markdown("But these departments might also be work")
