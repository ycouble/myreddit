import html
import re
from typing import Dict

from textacy import preprocessing


def replace_md_url(text):
    return re.compile(r"\[(.*)\]\(([^\(\)\[\]]*)\)").sub(r"\g<1> \g<2>", text)


preprocessing_pipeline = preprocessing.make_pipeline(
    html.unescape,
    html.unescape,
    preprocessing.normalize.whitespace,
    preprocessing.normalize.bullet_points,
    preprocessing.normalize.hyphenated_words,
    replace_md_url,
    preprocessing.replace.urls,
    preprocessing.remove.brackets,
    preprocessing.normalize.unicode,
    preprocessing.remove.accents,
    preprocessing.replace.emojis,
    preprocessing.replace.numbers,
    preprocessing.replace.user_handles,
)


def preprocess(data: Dict[str, str], field="selftext", new_field="text"):
    data = data.copy()
    text = data.pop("selftext")
    data["text"] = preprocessing_pipeline(text)
    return data
