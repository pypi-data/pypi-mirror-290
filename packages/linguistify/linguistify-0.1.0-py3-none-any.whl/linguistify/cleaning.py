import pandas as pd
import re
import string
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


def clean_text(text):
    """
    Cleans and preprocesses the input text by replacing symbols and emojis with words, removing unwanted characters,
    and applying stemming.

    Parameters:
    - text (str): The input text string to clean and preprocess.

    Returns:
    - str: The cleaned and preprocessed text string.
    """

    import nltk

    nltk.download("stopwords", quiet=True)

    # Create translation table to remove punctuation
    translate_table = str.maketrans("", "", string.punctuation)

    # Regular expressions for URL, IP address, hashtags, mentions, and emojis
    re_url = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
    re_ip = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
    re_hashtag = re.compile(r"#(\w*)")
    re_mention = re.compile(r"@(\w*)")
    re_emoji = re.compile(r":\)|:\(|:D|:P|:O|;D|:3|:\/|:S|:B|<3")

    # Emoji replacements
    emoji_replacements = {
        ":)": "happy",
        ":(": "sad",
        ":D": "laughing",
        ":P": "playful",
        ":O": "surprised",
        ";D": "wink",
        ":3": "cute",
        ":S": "worried",
        ":B": "cool",
        "<3": "love",
    }

    # Apply text transformations
    text = re_url.sub("URL", text)
    text = re_ip.sub("IPADDRESS", text)
    text = re_hashtag.sub(
        r"hashtag \1", text
    )  # Replace hashtags with "hashtag" + the hashtag text
    text = re_mention.sub(
        r"mention \1", text
    )  # Replace mentions with "mention" + the mention text

    # Replace emojis with textual equivalents
    for emoji, replacement in emoji_replacements.items():
        text = text.replace(emoji, replacement)

    text = text.translate(translate_table)  # Remove punctuation
    text = text.lower()  # Convert to lowercase

    # Tokenize the text and remove stopwords
    tokens = text.split()
    stops = set(stopwords.words("english"))
    tokens = [word for word in tokens if word not in stops and len(word) >= 3]

    # Apply basic text replacements
    replacements = {
        r"what's": "what is",
        r"\'s": " ",
        r"\'ve": " have",
        r"n't": " not",
        r"i'm": "i am",
        r"\'re": " are",
        r"\'d": " would",
        r"\'ll": " will",
        r"\'t": " not",
        r",": " ",
        r"\.": " ",
        r"!": " ! ",
        r"/": " ",
        r"\^": " ^ ",
        r"\+": " + ",
        r"\-": " - ",
        r"\=": " = ",
        r"'": " ",
        r"(\d+)(k)": r"\1" + "000",
        r":": " : ",
        r"e - mail": "email",
        r"\s{2,}": " ",
    }

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    # Final tokenization and stemming
    tokens = text.split()
    stemmer = SnowballStemmer("english")
    stemmed_words = [stemmer.stem(word) for word in tokens]

    return " ".join(stemmed_words)
