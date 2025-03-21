import marimo

__generated_with = "0.11.13"
app = marimo.App(width="medium")


@app.cell
def _():
    from sentence_transformers import SentenceTransformer, CrossEncoder, util
    import pandas as pd
    import marimo as mo
    return CrossEncoder, SentenceTransformer, mo, pd, util


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

        **Optional**

        A cross-encoder is significantly more taxing, so we'll use it as a means of re-ranking the top 5 results of the semantic search.

        See https://www.sbert.net/examples/applications/cross-encoder/README.html for more information
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Improving results

        Our main dataset is the contacts table. The department name and keyword is what is used to compare against a user's query or an existing FOIA's description.

        The accuracy of returning the correct deparment solely depends on providing the right keywords for the department. Better context could also be applied for what each department does
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Keyword Extraction

        Grab the keywords from the description of a FOIA and add it as a new column for better insights
        """
    )
    return


@app.cell
def _(foia_cleaned_df):
    from keybert import KeyBERT

    kw_model = KeyBERT()
    for index, foo in foia_cleaned_df.iterrows():
        keywords = kw_model.extract_keywords(foo['Request Description'], stop_words=["amtrak", "documents"], use_mmr=True)
        foia_cleaned_df.at[index, "keywords"] = ', '.join([kw[0] for kw in keywords])
    return KeyBERT, foo, index, keywords, kw_model


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Categorizing FOIA by their respective department via cosine similarity

        #### FOIA data

        It contains the following headings:

        - `Request ID`
        - `Request Description`

        #### Department data

        It contains the following headings: 

        - `Department`
        - `Keywords`
        - `Name`

        We'll have a list called data_row which contains a concatenation of a department and its keyword
        """
    )
    return


@app.cell
def _(foia_df):
    # foia_csv['keywords'] = foia_csv['Request Description'].apply(lambda x: ', '.join(keyword[0] for keyword in kw_model.extract_keywords(x, stop_words=["amtrak", "foia", "document"])))
    foia_df
    return


@app.cell
def _(kw_model, test_csv):
    test_csv['keywords'] = test_csv['Request Description'].apply(lambda x: ', '.join(keyword[0] for keyword in kw_model.extract_keywords(x, use_mmr=True, stop_words=["amtrak", "foia", "documents"])))
    return


@app.cell
def _(test_csv):
    test_csv
    return


@app.cell
def _(pd):
    test_csv = pd.read_csv("./data/contacts.csv", usecols=["test", "name"]).dropna().merge(pd.read_csv("./data/foia.csv"), left_on="test", right_on="Request ID")[['test', 'Request Description', 'name']]
    return (test_csv,)


@app.cell
def _(test_csv):
    test_csv
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Data Cleanup

        There are FOIAs that contain the following keywords:

        - “Duplicate”
        - “Not a proper FOIA request”
        - “unclear”
        """
    )
    return


@app.cell
def _(pd):
    foia_df = pd.read_csv('./data/foia.csv')
    foia_cleaned_df = foia_df[~foia_df['Request Description'].str.contains('|'.join(["Duplicate", "Not a proper FOIA request", "unclear"]), case=False, na=False)]
    deparment_df = pd.read_csv('./data/department.csv', encoding='latin-1').fillna('')
    return deparment_df, foia_cleaned_df, foia_df


@app.cell
def _(mo):
    mo.md(r"""### Encode department data""")
    return


@app.cell
def _(SentenceTransformer, deparment_df):
    bi_encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    dep_corpus = []
    for _, dep_data in deparment_df.iterrows():
        row = f"{dep_data["Department"]}/{dep_data["Keywords"]}"
        print(row)
        dep_corpus.append(row)

    query_embeddings = bi_encoder.encode(dep_corpus)
    return bi_encoder, dep_corpus, dep_data, query_embeddings, row


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Encode FOIA and compare

        Encode the description and its generated keywords

        We then map the department that has a cosine similarity score of **40%** else, we set it as unknown.
        """
    )
    return


@app.cell
def _(bi_encoder, dep_corpus, foia_cleaned_df, query_embeddings, util):
    for idx, data in foia_cleaned_df.iterrows():
        foia_row = f"{data['Request Description']}/{data['keywords']}"
        foia_encoding = bi_encoder.encode(foia_row)
        hit = util.semantic_search(foia_encoding, query_embeddings, top_k=1)
        dep_idx = hit[0][0]['corpus_id']
        score = hit[0][0]['score']
        foia_cleaned_df.at[idx, 'department'] = f"{dep_corpus[dep_idx].split('/')[0]}" if score > .40 else "Uknown"
    return data, dep_idx, foia_encoding, foia_row, hit, idx, score


@app.cell
def _(mo):
    mo.md(r"""### Comparison between exact word matching and semantic search""")
    return


@app.cell
def _(pd):
    exact_match_df = pd.read_csv("./data/exact_match.csv")
    semantic_search_df = pd.read_csv("./data/semantic_search.csv")
    return exact_match_df, semantic_search_df


@app.cell
def _(exact_match_df):
    import altair as alt
    alt.Chart(exact_match_df['departments'].value_counts().reset_index()).mark_arc().encode(
        theta="count",
        color="departments",
        tooltip=["departments", "count"]
    )


    return (alt,)


@app.cell
def _(alt, semantic_search_df):
    alt.Chart(semantic_search_df['department'].value_counts().reset_index()).mark_arc().encode(
        theta="count",
        color="department",
        tooltip=["department", "count"]
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
