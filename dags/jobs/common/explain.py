import shap
import spacy


def get_shap_explainer_for_spacy_textcat(model: spacy.language.Language):
    tokenizer = spacy.tokenizer.Tokenizer(model.vocab)
    # Run the spacy pipeline on some random text just to retrieve the classes
    doc = model("hi")
    class_names = list(doc.cats.keys())

    # Define a function to predict
    def predict(texts):
        # convert texts to bare strings
        texts = [str(text) for text in texts]
        results = []
        for doc in model.pipe(texts):
            # results.append([{'label': cat, 'score': doc.cats[cat]} for cat in doc.cats])
            results.append([doc.cats[cat] for cat in class_names])
        return results

    # Create a function to create a transformers-like tokenizer to match shap's expectations
    def tok_adapter(text, return_offsets_mapping=False):
        doc = tokenizer(text)
        out = {"input_ids": [tok.norm for tok in doc]}
        if return_offsets_mapping:
            out["offset_mapping"] = [(tok.idx, tok.idx + len(tok)) for tok in doc]
        return out

    # Create the Shap Explainer
    # - predict is the "model" function, adapted to a transformers-like model
    # - masker is the masker used by shap, which relies on a transformers-like tokenizer
    # - algorithm is set to permuation, which is the one used for transformers models
    # - output_names are the classes (altough it is not propagated to the permutation
    #   explainer currently, which is why plots do not have the labels)
    # - max_evals is set to a high number to reduce the probability of cases where the
    #   explainer fails because there are too many tokens
    explainer = shap.Explainer(
        predict,
        masker=shap.maskers.Text(tok_adapter),
        algorithm="permutation",
        output_names=class_names,
        max_evals=1500,
    )

    return explainer, class_names
