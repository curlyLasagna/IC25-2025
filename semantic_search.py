import marimo

__generated_with = "0.11.13"
app = marimo.App(width="medium")


@app.cell
def _():
    from sentence_transformers import SentenceTransformer, CrossEncoder, util
    import pandas as pd
    import marimo as mo
    import altair as alt
    return CrossEncoder, SentenceTransformer, alt, mo, pd, util


@app.cell
def _(mo):
    mo.md(r"""Previous FOIA cases will be used as test values""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        User queries are embeded so a cosine similarity may be performed between a user's query (FOIAs) and values from the vector store (list of departments and their respective keywords)
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

        Our main dataset is the departments table. The department name and keyword is what is used to compare against a user's query or an existing FOIA's description.

        The accuracy of returning the correct deparment solely depends on providing the right keywords for the department. 

        Better context could also be applied for what each department does
        """
    )
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
    foia_df = pd.read_csv('./data/pii/foia.csv')
    foia_cleaned_df = foia_df[~foia_df['Request Description'].str.contains('|'.join(["Duplicate", "Not a proper FOIA request", "unclear", "See attached"]), case=False, na=False)]
    return foia_cleaned_df, foia_df


@app.cell
def _(pd):
    deparment_df = pd.read_csv('./data/departments.csv', encoding='latin-1').fillna('')
    return (deparment_df,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Keyword Extraction

        Grab the keywords from the description of a FOIA and add it as a new column for better insights

        #### Stop words

        Stop words are words such as 'the', 'is', 'are', 'in', 'and' which are frequent words, but offer little value

        This is a means of reducing the amount of noise from our data.
        """
    )
    return


@app.cell
def _(foia_cleaned_df):
    from keybert import KeyBERT

    kw_model = KeyBERT()
    for index, foo in foia_cleaned_df.iterrows():
        keywords = kw_model.extract_keywords(foo['Request Description'], stop_words=["amtrak", "documents", "seeks", "english", "request"], use_mmr=True, keyphrase_ngram_range=(1,1))
        foia_cleaned_df.at[index, "keywords"] = ','.join([kw[0].strip() for kw in keywords])
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
def _(pd):
    test_csv = pd.read_csv("./data/contacts.csv", usecols=["test", "name"]).dropna().merge(pd.read_csv("./data/foia.csv"), left_on="test", right_on="Request ID")[['test', 'Request Description', 'name']]
    return (test_csv,)


@app.cell
def _(kw_model, test_csv):
    test_csv['keywords'] = test_csv['Request Description'].apply(lambda x: ','.join(keyword[0] for keyword in kw_model.extract_keywords(x, use_mmr=True, stop_words=["amtrak", "foia", "documents"])))
    return


@app.cell
def _(mo):
    mo.md(r"""### Encode department data""")
    return


@app.cell
def _(SentenceTransformer, deparment_df):
    bi_encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    dep_corpus = []
    for _, dep_data in deparment_df.iterrows():
        row = f"{dep_data["Department"]}|{dep_data["Keywords"]}"
        dep_corpus.append(row)
    query_embeddings = bi_encoder.encode(dep_corpus)
    return bi_encoder, dep_corpus, dep_data, query_embeddings, row


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Encode FOIA and compare

        Encode the description and its generated keywords

        This process takes a lot of time as it has to encode and compare 4k FOIAs

        We then map the department that has a cosine similarity score of **.50** else, we set it as unknown.
        """
    )
    return


@app.cell
def _(bi_encoder, dep_corpus, foia_cleaned_df, query_embeddings, util):
    for idx, data in foia_cleaned_df.iterrows():
        # Concatenate request description and the keywords generated 
        foia_row = f"{data['Request Description']}"
        foia_encoding = bi_encoder.encode(foia_row)
        hit = util.semantic_search(foia_encoding, query_embeddings, top_k=1)
        dep_idx = hit[0][0]['corpus_id']
        score = hit[0][0]['score']
        foia_cleaned_df.at[idx, 'department'] = f"{dep_corpus[dep_idx].split('|')[0]}" if score > .30 else "Unknown"
    return data, dep_idx, foia_encoding, foia_row, hit, idx, score


@app.cell
def _(mo):
    mo.md(r"""### Comparison between exact word matching and semantic search""")
    return


@app.cell
def _(alt, foia_cleaned_df):
    base_dep = alt.Chart(foia_cleaned_df['department'].value_counts().reset_index().nlargest(5, 'count')).encode(
        theta=alt.Theta("count").stack(True),
        color=alt.Color("department", scale=alt.Scale(scheme='category20c')).legend(None),
        tooltip=["department", "count"]
    )
    dep_pie = base_dep.mark_arc()

    dep_label = base_dep.mark_text(size=12, radius=175, limit=140).encode(text='department', color=alt.value('black'))

    (dep_pie + dep_label)
    # (dep_pie + dep_label).save('departments.html')
    return base_dep, dep_label, dep_pie


@app.cell
def _(foia_cleaned_df):
    dep_frames = {}
    for dep in foia_cleaned_df['department'].unique():
        dep_frames[dep] = foia_cleaned_df[foia_cleaned_df['department'] == dep]
    return dep, dep_frames


app._unparsable_cell(
    r"""
    alt.Chart(dep_frames[\"Uknown\"]['keywords']
              .str.split(',')
              .explode()
              .value_counts()
              .reset_index(),
              title = \"Keywords for uncategorized FOIA\"
             ).mark_bar().encode(
        x=alt.X('keywords', axis=alt.Axis(labelAngle=-45)).sort('-y'),
        y=alt.Y('count')
    ).properties(autosize="fit", width=1200).transform_filter(alt.FieldGTPredicate(field="count", gt=20)).save('unknown.html')

    """,
    name="_"
)


@app.cell
def _(dep_frames):
    dep_frames["Uknown"]['keywords'].str.split(',').explode().value_counts()
    return


@app.cell
def _(dep_frames):
    dep_frames["Amtrak PD"]['keywords'].str.split(',').explode().value_counts()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
