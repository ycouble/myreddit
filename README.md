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


``` flowchart
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
