# UMD IC25 - Amtrak FOIA Data Analysis (04)

## Results

The results of the processed FOIA data is available in the [`results.csv`](./results.csv) file.

## Unprocessed Data

All raw and unprocessed data belongs in the `data/` directory, which is
then processed by the `src/to_csv.py`, `src/classification.py`, and `src/semantic_search.py`
scripts to produce results.

Here are the files required for processing:

- A CSV file of all FOIA requests - `data/pii/data.csv` (not included in repo)
- A list of all departments - [`data/departments.csv`](./data/departments.csv)

There is also some information that includes personally identifiable information,
also known as PII. This data is stored in the `data/pii/` directory, which
unfortunately includes the actual *un-processed* FOIA dataset

## Use of AI

Generative AI was heavily used throughout this project
|                 |                                                                                                                                                          |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Platform        | Google AI Studio. Gemini 2.0 Flash model                                                                                                                 |
| How it was used | Explain concepts concisely. How to generate a chart using Altair. Debug through errors. Determine where a keyword should go based on a department's name |
| Learning points | Filtering dataframes. Applying functions to each row of a dataframe. What stop words are in the context of keyword extraction. Libraries to to use       |

## Notebook

### Dependencies
`uv sync`

### Run notebook
> Make sure a venv is created and activated

`marimo edit semantic_search.py`