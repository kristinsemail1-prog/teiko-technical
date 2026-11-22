# Teiko Technical Assessment

This project analyzes immune-cell population data from a clinical trial using Python, SQLite, pandas, and Streamlit.

## Project overview

Part 1: Create a SQLite database from the `cell-count.csv` file.
Part 2: Calculate the frequency of each cell population within each sample to get percentage of each cell type in the sample.
Part 3: Compare melanoma PBMC samples treated with miraclib between responders and non-responders using a two-sample t-test.
Part 4: Identify melanoma PBMC samples at treatment time 0 from patients treated with miraclib and summarize projects, response, and sex.

## Setup

Install the required packages:

```
make setup
```

## Run the data pipeline

```
make pipeline
```

## Run the dashboard

```
make dashboard
```

Open the dashboard at [Teiko dashboard](https://teiko-technical-gxe49jn99frast6hll7nkb.streamlit.app/)

## Project files

- `load_data.py` creates the SQLite database and loads the CSV data.
- `Analysis.py` completes the Part 2, 3, and 4 analyses.
- `app.py` displays the interactive dashboard.
- `requirements.txt` lists the required Python packages.
- `Makefile` provides the setup, pipeline, and dashboard commands.