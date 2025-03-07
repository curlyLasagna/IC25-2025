import pandas as pd
from sentence_transformers import CrossEncoder, SentenceTransformer, util

bi_encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
corpus = []


def embed_contacts():
    global corpus
    corpus = []
    contacts_df = pd.read_csv(
        "./data/contacts.csv",
        usecols=lambda x: x.lower() in ["name", "department", "keywords"],
        # So much random encoding issues -_-
        encoding="latin-1",
    )

    # Store each row to vector datastore
    for _, data in contacts_df.iterrows():
        # Use `/` as a delimiter
        row = f"{data['name']}/{data['department']}/{data['keywords']}"
        corpus.append(row)
    # Embed list of rows into an in-memory vector store
    return bi_encoder.encode(corpus)


def query_vector(user_query: str) -> list[str]:
    hits = util.semantic_search(
        bi_encoder.encode([user_query]), embed_contacts(), top_k=10
    )[0]
    # Only return the name
    return [f"{corpus[hit['corpus_id']].split('/')[0]}" for hit in hits]
