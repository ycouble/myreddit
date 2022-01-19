[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pre-commit/pre-commit/master.svg)](https://results.pre-commit.ci/latest/github/pre-commit/pre-commit/master)

# My Reddit: an exploratory NLP project on reddit

## Feature Ideas

- Dashboard of each subreddit summary (nb posts, topics, nb votes, etc.)
- Topic modelling
- Automatic text preprocessing (pipelines)
- Text classification (types of posts, topic)
- Text summarization
- URL extractions
- Tech NER

## Data organization

### Data Lake

- Dagster Pipelines:
  - Scrapping
  - API calls
- Reddit raw data (html pages, json): **reddit_raw** --> document oriented DB (MongoDB)
- Potential complementary data: list of techs

### Data Warehouse

#### Ingestion / Preproc

- Dagster Pipelines
  - Parsing & Organization
    - Insert in relational DB
  - Preprocessing
    - Clean texts
    - Featurize
- Data Mart n°1: **reddit_db** (PostgreSQL)
- Feature Stores **reddit_features** or **reddit_db**
  - Spacy docs [storing spacy docs](https://spacy.io/usage/saving-loading#docs) (might not be useful)
  - Prodigy Annotations [using a custom DB](https://prodi.gy/docs/api-database#setup-postgresql)
  - Sentence Embeddings
  - Word Embeddings
  - Vector representations of docs

#### Data Mart

- Dagster Pipelines
  - Information Extraction / Aggregation
- Data Mart n°2: **reddit_insights** (PostgreSQL

## Code organization

- jobs/ (dagster pipelines)
  - ingest/ (scrapp + API calls) (web --> reddit_raw)
  - preproc/ (cleaning, featurizing, ...) (reddit_raw --> reddit_db (opt. --> reddit_insights))
  - app/ (reddit_db --> reddit_insights)

```flowchart
reddit=>start: Reddit website / API
ing=>operation: Ingestion
raw=>subroutine: Raw Data (reddit_raw)
db=>subroutine: Database (reddit_db)
ext=>operation: Extraction
ins=>subroutine: Insights (reddit_insights)
pre=>parallel: Preprocessing / Featurization

dash=>end: Dashboards

reddit->ing->raw
raw->pre
pre(path1, right)->ins
pre(path2, bottom)->db
db->ext->ins
ins->dash
```

## Service Architecture

- job_runner: AirFlow
- Data Connection: AirByte
- (Data Transformations: dbt)
- database: PostgreSQL
- API server: exposes http/https: FastAPI

Options:

- 4 dockerfiles, 1 docker compose (easy to redeploy)

- Cloud based (automated creation) --> at what price ?



#
