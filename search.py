from sentence_transformers import SentenceTransformer, CrossEncoder, util
import pandas as pd

bi_encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
corpus = []


def embed_contacts():
    contacts_df = pd.read_csv(
        "./data/contacts.csv",
        usecols=lambda x: x.lower() in ["name", "department", "keywords"],
        # wtf
        encoding="latin-1",
    )

    # Store each row
    for _, data in contacts_df.iterrows():
        row = f"{data['Name']} - {data['Department']}"
        corpus.append(row)
    # Embed list of rows into an in-memory vector store
    return bi_encoder.encode(corpus)


def query_vector(user_query: str) -> list[str]:
    hits = util.semantic_search(
        bi_encoder.encode([user_query]), embed_contacts(), top_k=10
    )[0]
    return [f"{corpus[hit['corpus_id']]}" for hit in hits]
