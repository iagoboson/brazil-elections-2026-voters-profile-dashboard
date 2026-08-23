# Brazil Elections 2026 — Electorate Profile

Interactive bilingual dashboard for exploring the demographic profile of Brazil’s 2026 electorate.

The application covers Brazil, all 26 states, the Federal District, and voters registered abroad. Users can filter by gender, age group, education, marital status, race/color, gender identity, Quilombola identification, and Brazilian Sign Language interpreter status.

## What the project demonstrates

- Exploratory data analysis with Python and pandas
- Processing and aggregation of multi-gigabyte CSV files
- A compact Parquet analytical dataset
- Interactive visualizations with Plotly
- A bilingual Streamlit application
- Transparent handling of missing and self-reported demographic data

## Run locally

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

## Data source

The source data is the official **Perfil do Eleitorado 2026** dataset published by Brazil’s Superior Electoral Court (TSE):

- [TSE Open Data Portal](https://dadosabertos.tse.jus.br/)
- Extraction date contained in the source files: July 14, 2026

Raw TSE files are not included because they occupy several gigabytes. The application uses an aggregated Parquet file derived from the official data.

## Important limitations

- Each source row represents an aggregated demographic profile, not an individual voter.
- Demographic attributes are self-reported and may not reflect recent changes.
- Race/color, gender identity, Quilombola identification, and interpreter status contain substantial volumes of `Not informed` records.
- The data can be revised by the TSE after publication.
- This is a nonpartisan exploratory project and does not predict election outcomes.

## Technology

Python · pandas · Plotly · Streamlit · Parquet
