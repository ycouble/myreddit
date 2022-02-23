import spacy_streamlit

models = ["en_core_web_sm", "en_core_web_md"]
default_text = (
    "PALO IT is a global innovation consultancy and Agile software development "
    "company dedicated to helping organizations embrace tech as a force for good."
)
spacy_streamlit.visualize(models, default_text)
