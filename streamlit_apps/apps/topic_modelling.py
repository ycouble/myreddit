from pathlib import Path

import pyLDAvis
import pyLDAvis.gensim_models
import streamlit as st
import streamlit.components.v1 as components
from gensim.corpora import Dictionary, MmCorpus
from gensim.models import LdaModel

ROOT_DIR = Path("/opt/streamlit")


def get_model_name(num_topics, use_bigrams, bigrams_min_count, no_below, no_above):
    return f"lda_{num_topics}topics_{no_below}_{no_above}_{'bi'+str(bigrams_min_count) if use_bigrams else 'nobi'}"


def load_model(name):
    model_type = "topics"
    config_name = name
    model_folder = ROOT_DIR / "models" / model_type / config_name
    date = ""
    for _ in ["year", "month", "day"]:
        max_date = max(x.name for x in model_folder.iterdir() if x.is_dir())
        model_folder = model_folder / max_date
        date += "/" + max_date
    model = LdaModel.load(str(model_folder / "model"))
    dictionary = Dictionary.load(str(model_folder / "dictionary"))
    corpus = MmCorpus(str(model_folder / "corpus"))
    return (
        model,
        dictionary,
        corpus,
    )


st.title("Topic Modeling")
num_topics = st.select_slider("Number of topics", options=[5, 10, 20, 50], value=10)
use_bigrams = st.checkbox("Use bi-grams in the dictionary", value=False)
bigrams_min_count = st.select_slider(
    "Minimum count to accept bigram in Dictionary",
    options=[5, 20],
    value=20,
    disabled=not use_bigrams,
)
no_below = st.select_slider(
    "Minimum number of appearance of a word to include in dictionary",
    options=[5, 10, 20, 50],
    value=10,
)
no_above = st.select_slider(
    "Maximum ratio of document appearances of a word to include in dictionary",
    options=[0.5, 0.99],
    value=0.5,
    format_func=lambda x: f"{round(100*x)}%",
)

model, dictionary, corpus = load_model(
    get_model_name(num_topics, use_bigrams, bigrams_min_count, no_below, no_above)
)

vis_data = pyLDAvis.gensim_models.prepare(model, corpus, dictionary)
components.html(
    "<div style='background-color:white'>"
    + pyLDAvis.prepared_data_to_html(vis_data)
    + "</div>",
    width=1300,
    height=800,
    scrolling=False,
)
