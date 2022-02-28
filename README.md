[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pre-commit/pre-commit/master.svg)](https://results.pre-commit.ci/latest/github/pre-commit/pre-commit/master)

# My Reddit: an exploratory NLP project on reddit data
This is a demonstrator project of a fully featured NLP/ML system.

This project covers from data extraction to dashboarding to MLOps.

```mermaid
flowchart TD
    %% EL[T]
    reddit[[Reddit API]] --- ELT[\Extract Load - python/dagster/]
    ELT --> posts{{posts + comments}}
    %% [EL]T DBT processes
    posts --- pdbt[\Transform - DBT/]
    pdbt --> stats{{Statistics}}
    pdbt --> txt{{Texts}}
    %% Dashboards
    stats --- cube[\Aggregation/DataViz - Cube JS/] --> Dashboards
    %% Clean texts
    txt --- textacy[\Preprocessing - Textacy/] --> clean{{Clean Texts}}
    %% Subreddit prediction (trivial)
    txtcattr[\Train - Spacy/Transformers/] --> perfs{{Performances}}
    perfs --- cube
    clean --- txtcattr --> srmodel([Models])
    clean --- txtcatpr[\Batch Predictions/] --> prtxtcat{{Predictions}}
    srmodel --- txtcatpr
    %% APIs
    srmodel --> modelapi[[Prediction API - FastAPI]]
    %% Apps
    srmodel --> apps[Applications - Streamlit]
    clean --> apps
```
Legend:
```mermaid
flowchart TD
    legendapi[[API]]
    legendtr[\Transformation/]
    legenddb{{Data}}
    ledendweb[Web UI]
```
## Architecture

![architecture](assets/architecture.png)

## Features

### NLP Features
Implemented:
- Syntactic analysis with Spacy
- Topic Modeling with BERTopic
- Text classification with custom model

Coming Soon:
- Language detection
- Topic Modeling algorithm comparison

### Product
- A dashboard app based on cubeJS
- A frontend which integrates all administration web UIs
- Data collection on demand & on schedules
- Cloud Database (BigQuery)
- On demand & scheduled model training
- APIs to serve models
- MLOps for NLP with explainability
- Interactive Apps
