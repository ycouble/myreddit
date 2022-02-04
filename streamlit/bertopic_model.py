import random

from bertopic import BERTopic
from google.cloud import bigquery
from google.oauth2 import service_account

# import spacy_streamlit
import streamlit as st

key_path = "/Users/yco/.config/dbt-user-creds.json"
credentials = service_account.Credentials.from_service_account_file(
    key_path  # , scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
client = bigquery.Client(
    credentials=credentials,
    project=credentials.project_id,
)


@st.cache
def get_model(docs, max_ngram):
    model = BERTopic.load("models/bertopic/distilbert/model")
    # topics, _ = model.transform(docs)
    # print(topics)
    # model.update_topics(docs, topics, n_gram_range=(1, max_ngram))
    topics, probs = model.transform(docs)
    return model, topics, probs


@st.cache
def get_sample_data():
    data = list(client.query(f"SELECT * FROM `reddit_texts.posts_clean`"))
    data = random.choices([row for row in data], k=10)
    return list(d["text"] for d in data)


@st.cache
def predict(model, docs):
    return


# model.update_topics(docs, topics, n_gram_range=(1, 5))


st.header("Topic Modeling With BERTopic")

st.write(
    "BERTopic is a topic modeling technique that leverages 🤗 transformers and a custom class-based TF-IDF to create dense clusters allowing for easily interpretable topics whilst keeping important words in the topic descriptions."
)

st.write(
    "We trained a BERTopic on our Reddit Data Science dataset, to see how the BERTopic model is able to discriminate the topics"
)

st.subheader("Tune model")
st.write("It is possible to fine-tune the last part of the mode (c-TF-TDF)")

max_ngram = st.number_input(
    "max_ngram parameter", value=3, step=1, max_value=10, min_value=2
)

docs = get_sample_data()
model, topics, probs = get_model(docs, max_ngram)

st.subheader("Topic repartition")
st.table(model.get_topic_info())
st.plotly_chart(model.visualize_barchart(top_n_topics=10))

st.subheader("Topic Similarities")
st.plotly_chart(model.visualize_topics())

st.subheader("Topic probability Disctribution for a given text")
text = st.selectbox("Choose a text", options=docs)
text_id = docs.index(text)
st.write("Sample text:")
st.write(text)
st.plotly_chart(model.visualize_distribution(probs[text_id], min_probability=0.015))

st.subheader("Hierarchical clustering")
st.plotly_chart(model.visualize_hierarchy(top_n_topics=50))

st.subheader("Topic Similarities")
st.plotly_chart(model.visualize_heatmap(n_clusters=8, width=1000, height=1000))
