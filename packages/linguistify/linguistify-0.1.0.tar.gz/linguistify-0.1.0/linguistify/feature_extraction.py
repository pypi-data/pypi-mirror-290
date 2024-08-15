import pandas as pd
import re
import string
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords


def add_features_to_dataframe(df, text_column):
    """
    Adds various text-based features to a DataFrame by extracting information from a specified text column.

    This function performs feature extraction on the text data in the specified column of the DataFrame.
    It calculates several features such as text length, number of stop words, digits, spaces, and punctuation marks.
    Additionally, it provides counts of different parts of speech (POS) including adjectives, nouns, pronouns,
    verbs, and adverbs.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the text data.
    - text_column (str): The name of the column in the DataFrame that contains the text data to analyze.

    Returns:
    - pd.DataFrame: The original DataFrame with additional columns for the extracted features.

    Raises:
    - ValueError: If the specified text_column does not exist in the DataFrame.

    Downloads:
    - NLTK Data: 'punkt', 'averaged_perceptron_tagger', and 'stopwords'.

    Feature Extraction Functions:
    - length_of_text(text): Returns the length of the text.
    - num_stop_words(text): Returns the count of stop words in the text.
    - num_digits(text): Returns the count of digit characters in the text.
    - num_spaces(text): Returns the count of space characters in the text.
    - num_exclamations(text): Returns the count of exclamation marks in the text.
    - num_questions(text): Returns the count of question marks in the text.
    - num_periods(text): Returns the count of period characters in the text.
    - pos_tag_counts(text): Returns a dictionary with counts of adjectives, nouns, pronouns, verbs, and adverbs.
    """

    # Check if the text_column exists in the DataFrame
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in the DataFrame")

    # Download necessary NLTK data
    import nltk

    nltk.download("punkt")
    nltk.download("averaged_perceptron_tagger")
    nltk.download("stopwords")

    stop_words = set(stopwords.words("english"))

    # Feature extraction functions
    def length_of_text(text):
        """
        Calculates the length of the text.

        Parameters:
        - text (str): The text to measure.

        Returns:
        - int: The length of the text.
        """
        return len(text)

    def num_stop_words(text):
        """
        Counts the number of stop words in the text.

        Parameters:
        - text (str): The text to analyze.

        Returns:
        - int: The count of stop words in the text.
        """
        words = word_tokenize(text)
        return sum(1 for word in words if word.lower() in stop_words)

    def num_digits(text):
        """
        Counts the number of digit characters in the text.

        Parameters:
        - text (str): The text to analyze.

        Returns:
        - int: The count of digits in the text.
        """
        return sum(c.isdigit() for c in text)

    def num_spaces(text):
        """
        Counts the number of space characters in the text.

        Parameters:
        - text (str): The text to analyze.

        Returns:
        - int: The count of spaces in the text.
        """
        return text.count(" ")

    def num_exclamations(text):
        """
        Counts the number of exclamation marks in the text.

        Parameters:
        - text (str): The text to analyze.

        Returns:
        - int: The count of exclamation marks in the text.
        """
        return text.count("!")

    def num_questions(text):
        """
        Counts the number of question marks in the text.

        Parameters:
        - text (str): The text to analyze.

        Returns:
        - int: The count of question marks in the text.
        """
        return text.count("?")

    def num_periods(text):
        """
        Counts the number of period characters in the text.

        Parameters:
        - text (str): The text to analyze.

        Returns:
        - int: The count of periods in the text.
        """
        return text.count(".")

    def pos_tag_counts(text):
        """
        Counts the number of different parts of speech (POS) in the text.

        Parameters:
        - text (str): The text to analyze.

        Returns:
        - dict: A dictionary with counts of adjectives (JJ), nouns (NN), pronouns (PR), verbs (VB), and adverbs (RB).
        """
        words = word_tokenize(text)
        tagged = pos_tag(words)
        counts = {
            "num_adjectives": sum(1 for word, pos in tagged if pos.startswith("JJ")),
            "num_nouns": sum(1 for word, pos in tagged if pos.startswith("NN")),
            "num_pronouns": sum(1 for word, pos in tagged if pos.startswith("PR")),
            "num_verbs": sum(1 for word, pos in tagged if pos.startswith("VB")),
            "num_adverbs": sum(1 for word, pos in tagged if pos.startswith("RB")),
        }
        return counts

    # Apply the feature extraction functions to the specified column
    df["length_of_text"] = df[text_column].apply(length_of_text)
    df["num_stop_words"] = df[text_column].apply(num_stop_words)
    df["num_digits"] = df[text_column].apply(num_digits)
    df["num_spaces"] = df[text_column].apply(num_spaces)
    df["num_exclamations"] = df[text_column].apply(num_exclamations)
    df["num_questions"] = df[text_column].apply(num_questions)
    df["num_periods"] = df[text_column].apply(num_periods)

    # Expand the POS tag counts into separate columns
    pos_counts = df[text_column].apply(pos_tag_counts)
    df = df.join(pd.DataFrame(pos_counts.tolist()))

    return df
