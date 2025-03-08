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
unfortunately includes the actual _un-processed_ FOIA dataset

## Use of AI

Generative AI was heavily used throughout this project

|                 |                                                                                                                                                          |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Platform        | Google AI Studio. Gemini 2.0 Flash model                                                                                                                 |
| How it was used | Explain concepts concisely. How to generate a chart using Altair. Debug through errors. Determine where a keyword should go based on a department's name |
| Learning points | Filtering dataframes. Applying functions to each row of a dataframe. What stop words are in the context of keyword extraction. Libraries to use          |

## Usage

To utilize the Python programs used to complete this project, you must,

1. Have Python 3.13 installed
2. Have 'uv' package manager installed, available here: https://docs.astral.sh/uv/#installation

### Getting started

First, install all the required packages using uv:

```sh
$ uv sync # Installs the necessary packages
```

Then pull a copy of all FOIAs (or a subset) in CSV format, and save it in [`./data/pii/data.csv`](./data/pii).

> [!WARNING]
>
> Ensure the columns are in the following format: __`Request ID,Request Description`__

### Running the classification script

> [!WARNING]
>
> Ensure you're in the **ROOT DIRECTORY** of this repository when executing the script.

To run the classification script, run the following:

```sh
$ python3 src/classification.py
```

The results will appear in the [`results.csv`](./results.csv) file.

### Run notebook

> Make sure a venv is created and activated

`marimo edit semantic_search.py`

## Streamlit Prototype

To run a quick prototype of our search app that will return department that semantic search considers as the best candidate

`streamlit run search_app.py`
