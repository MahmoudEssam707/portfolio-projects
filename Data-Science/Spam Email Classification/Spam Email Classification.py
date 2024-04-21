# Description: This file contains the code for the GUI of the spam classifier. The GUI is built using the Flet library.
# The GUI allows the user to input a text message and then classify it as spam or not spam using the pre-trained model.
# The model is loaded from the spam_classifier.pkl file and the pre-fitted vectorizers are loaded from the vectorizer.pkl and tfidf_transformer.pkl files.
# The input text is cleaned using the clean_text function and then transformed using the loaded vectorizer and tfidf_transformer.
# The cleaned and transformed text is then passed to the model for classification.
# The classification result is displayed on the GUI as "Spam" or "Not Spam".
import re
import flet as ft
from joblib import load
import pandas as pd
from nltk.corpus import stopwords

total_stop_words = (
    stopwords.words("english")
    + stopwords.words("spanish")
    + stopwords.words("french")
    + [
        "ur",
        "im",
        "dont",
        "doin",
        "ure",
        "2",
        "4",
        "r",
        "u",
        "n",
        "lt",
        "gt",
        "amp",
        "ok",
        "pls",
        "v",
        "c",
        "n",
        "b",
        "wk",
        "th",
        "nd",
        "st",
        "rd",
        "th",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "ab",
        "ac",
        "ad",
        "ae",
        "af",
        "ag",
        "ah",
        "ai",
        "aj",
        "ak",
        "al",
        "am",
        "an",
        "ao",
        "ap",
        "aq",
        "ar",
        "as",
        "at",
        "au",
        "av",
        "aw",
        "ax",
        "ay",
        "az",
        "ba",
        "bb",
        "bc",
        "bd",
        "be",
        "bf",
        "bg",
        "bh",
        "bi",
        "bj",
        "bk",
        "bl",
        "bm",
        "bn",
        "bo",
        "bp",
        "bq",
        "br",
        "bs",
        "bt",
        "bu",
        "bv",
        "bw",
        "bx",
        "by",
        "bz",
        "ca",
        "cb",
        "cc",
        "cd",
        "ce",
        "cf",
        "cg",
        "ch",
        "ci",
        "cj",
        "ck",
        "cl",
        "cm",
        "cn",
        "co",
        "cp",
        "cq",
        "cr",
        "cs",
        "ct",
        "cu",
        "cv",
        "cw",
        "cx",
        "cy",
        "cz",
        "da",
        "db",
        "dc",
        "dd",
        "de",
        "df",
        "dg",
        "dh",
        "di",
        "dj",
        "dk",
        "dl",
        "dm",
        "dn",
        "do",
        "dp",
        "dq",
        "dr",
        "ds",
        "dt",
        "du",
        "dv",
        "dw",
        "dx",
        "dy",
        "dz",
        "ea",
        "eb",
        "ec",
        "ed",
        "ee",
        "ef",
        "eg",
        "eh",
        "ei",
        "ej",
        "ek",
        "el",
        "em",
        "en",
        "eo",
        "ep",
        "eq",
        "er",
        "es",
        "et",
        "eu",
        "ev",
        "ew",
        "ex",
        "ey",
        "ez",
        "fa",
        "fb",
        "fc",
        "fd",
        "fe",
        "ff",
        "fg",
        "fh",
        "fi",
        "fj",
        "fk",
        "fl",
        "fm",
        "fn",
        "fo",
        "fp",
        "fq",
        "fr",
        "fs",
        "ft",
        "fu",
        "fv",
        "fw",
        "fx",
        "fy",
        "fz",
        "ga",
        "gb",
        "gc",
        "gd",
        "ge",
        "gf",
        "gg",
        "gh",
        "gi",
        "gj",
        "gk",
        "gl",
        "gm",
        "gn",
        "go",
        "gp",
        "gq",
        "gr",
        "gs",
        "gt",
        "gu",
        "gv",
        "gw",
        "gx",
        "gy",
        "gz",
        "ha",
        "hb",
        "hc",
        "hd",
        "he",
        "hf",
        "hg",
        "hh",
        "hi",
        "hj",
        "hk",
        "hl",
        "hm",
        "hn",
        "ho",
        "hp",
        "hq",
        "hr",
        "hs",
        "ht",
    ]
)

# Load the pre-trained model and the pre-fitted vectorizers
model = load("assets/spam_classifier.pkl")
vectorizer = load("assets/vectorizer.pkl")  # Load your pre-fitted CountVectorizer
tfidf_transformer = load(
    "assets/tfidf_transformer.pkl"
)  # Load your pre-fitted TfidfTransformer


def clean_text(text):
    # Define the total_stop_words inside the function or load it from an external file
    text = re.sub(r"[^\w\s]", "", text, re.UNICODE)
    text = text.lower()
    text = [word for word in text.split() if word not in total_stop_words]
    text = " ".join(text)
    return text


def Clean(text):
    text = clean_text(text)
    text = vectorizer.transform([text])  # Use the loaded, fitted vectorizer
    text = tfidf_transformer.transform(text)  # Use the loaded, fitted tfidf_transformer
    return pd.DataFrame(text.toarray())  # Convert to DataFrame for model input


def main(page: ft.Page):
    # UI Elements setup
    page.title = "SMS Spam Classifier"
    txt_input = ft.TextField(
        label="Enter SMS text",
        expand=True,
        autofocus=True,
        on_change=lambda e: classify_text(page, e.control),
    )


    lbl_output = ft.Text()  # Use Text, as Flet does not have Label

    def classify_text(page, txt_input):
        text = txt_input.value.strip()
        if text:
            clean_text = Clean(text)
            prediction = model.predict(clean_text)[0]  # Use the cleaned and transformed text
            prediction = "Spam" if prediction == 1 else "Not Spam"
            lbl_output.value = f"Classification: {prediction}"
        else:
            lbl_output.value = "Please enter some text to classify."
        page.update()

    page.add(txt_input, lbl_output)


ft.app(target=main)
