import random

import spacy
import spacy_streamlit
from google.cloud import bigquery
from google.oauth2 import service_account

import streamlit as st

key_path = "/Users/yco/.config/dbt-user-creds.json"
credentials = service_account.Credentials.from_service_account_file(
    key_path  # , scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = bigquery.Client(
    credentials=credentials,
    project=credentials.project_id,
)
query_job = client.query(f"SELECT * FROM `reddit_texts.posts_clean` LIMIT 500")
ids, data = list(
    zip(*list(enumerate(random.choices([dict(row) for row in query_job], k=10))))
)

spacy_model = st.selectbox("Spacy Model", options=["en_core_web_md"])
nlp = spacy.load(spacy_model)
labels = nlp.get_pipe("ner").labels
# Load the text categorization model from the trained model
nlp.add_pipe(
    "textcat",
    source=spacy.load("models/subreddit_classif/textcat_ens/2022/02/01/model-best"),
)

text = st.selectbox("Text to analyze", options=[d["text"] for d in data])
doc = nlp(text)


spacy_streamlit.visualize_ner(
    doc,
    labels=labels,
    show_table=False,
    title="Named Entity Recognition",
)

spacy_streamlit.visualize_textcat(
    doc,
    title="Text Categorization",
)
