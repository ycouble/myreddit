
# My Reddit: an exploratory NLP project on reddit data

This website is a fully featured demonstrator of a Natural Language Processing (NLP) application:
from data extraction to end user application, we've covered the whole lifecycle of a NLP application with a modern and open-source NLP data stack.

- The data is extracted from Reddit API, loaded into a [BigQuery](https://cloud.google.com/bigquery) DB.
- It is then locally transformed using [DBT](https://www.getdbt.com/)
- The texts are cleaned and preprocessed using [textacy](https://github.com/chartbeat-labs/textacy)
- Models are trained using [spaCy](https://spacy.io)
- Models are served using [FastAPI](https://fastapi.tiangolo.com/)
- Models are monitored and new unknown data is annotated through [Rubrix](https://www.rubrix.ml/)
- Model performance and data are monitored through dashboard made with [Metabase](https://www.metabase.com/)
- End user applications are demonstrated using [Streamlit](https://streamlit.io)
