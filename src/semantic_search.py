import marimo

__generated_with = "0.11.13"
app = marimo.App(width="medium")


@app.cell
def _():
    from sentence_transformers import SentenceTransformer, CrossEncoder, util
    import pandas as pd

    bi_encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    # cross_encoder = CrossEncoder("")
    return CrossEncoder, SentenceTransformer, bi_encoder, pd, util


@app.cell
def _(mo):
    mo.md(
        r"""
        Read in the contacts data.

        Each row contains a contact and their respective department.
        """
    )
    return


@app.cell
def _(bi_encoder, pd):
    contacts_df = pd.read_csv("data/contacts.csv", usecols= lambda x: x.lower() in ['name', 'department'])
    # Store each row 
    corpus = []
    for _, data in contacts_df.iterrows():
        row = f"{data['Name']} - {data['Department']}"
        corpus.append(row)
    # Embed list of rows into an in-memory vector store
    contact_embeddings = bi_encoder.encode(corpus, convert_to_tensor=False, show_progress_bar=True)
    import numpy as np
    contact_embeddings = contact_embeddings.astype(np.float32)
    return contact_embeddings, contacts_df, corpus, data, np, row


@app.cell
def _(mo):
    mo.md(r"""Previous FOIA cases will be used as test values""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        User queries are embeded so a cosine similarity may be performed between the query and values from the vector store
        ![](https://raw.githubusercontent.com/UKPLab/sentence-transformers/master/docs/img/Bi_vs_Cross-Encoder.png)

        A cross-encoder is significantly more taxing, so we'll use it as a means of re-ranking the top 5 results of the semantic search.

        See https://www.sbert.net/examples/applications/cross-encoder/README.html for more information
        """
    )
    return


@app.cell
def _(bi_encoder, np, test_queries):
    query_embedding = bi_encoder.encode([test_queries["Caruso"]], convert_to_tensor=False).astype(np.float32)
    return (query_embedding,)


@app.cell
def _(contact_embeddings, corpus, query_embedding, util):
    hits = util.semantic_search(query_embedding, contact_embeddings, top_k=10)
    for hit in hits[0]:
        print(f"{corpus[hit['corpus_id']]} with a score of {hit['score']:.2f}")
    return hit, hits


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Improving results

        Our main dataset is the contacts table.

        In order to improve the accuracy of the search engine, the contacts table can should be organized as such:

        | contact | department | keywords |
        |---------|------------|----------|
        |         |            |          |
        |         |            |          |
        |         |            |          |

        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Keyword Extraction

        """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
