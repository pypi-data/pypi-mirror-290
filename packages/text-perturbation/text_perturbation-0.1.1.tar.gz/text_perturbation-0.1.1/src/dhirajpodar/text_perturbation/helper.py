"""helper python file."""

import random
import re

from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import nltk

device = "cpu"


def get_synonyms(word):
    """Get synonyms of a word."""
    synonyms = set()

    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace("_", " ").replace("-", " ").lower()
            synonym = "".join(
                [
                    char
                    for char in synonym
                    if char in " qwertyuiopasdfghjklzxcvbnm"
                ]
            )
            synonyms.add(synonym)

    if word in synonyms:
        synonyms.remove(word)

    return list(synonyms)


def remove_stopwords(sentence):
    """Remove stopwords.

    returns a list of word without stop words.
    """
    words = word_tokenize(sentence)
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    if "." in filtered_words:
        filtered_words.remove(".")
    return filtered_words


def remove_punctuations(sentence) -> str:
    """Remove punctuations.

    return a sentence(str) removing all the punctuations.
    """
    punctuation_pattern = re.compile(r"[^\w\s]")
    return re.sub(punctuation_pattern, "", sentence)


def get_hypernyms(word):
    """Get hypernyms."""
    if wordnet.synsets(word):
        hypernym_word = wordnet.synsets(word)[0]
        if hypernym_word.hypernyms():
            hypernym = hypernym_word.hypernyms()[0]
            no_underscores = hypernym.name().split(".n")[0]
            return no_underscores.replace("_", " ")
    return word


def detokenize(encoded):
    """Detokenize text.

    returns sentence from list of words or tokens.
    """
    decoded = " ".join(encoded)
    return re.sub(r"\s+(?=[,'?.])", "", decoded)


def calculate_token_difference(questions, perturbated_questions):
    """Calculate the difference in words."""
    if questions == perturbated_questions:
        return 0

    questions_tokens = word_tokenize(questions)
    perturbated_questions_tokens = word_tokenize(perturbated_questions)

    set_tokens1 = set(questions_tokens)
    set_tokens2 = set(perturbated_questions_tokens)

    diff_tokens = set_tokens1.symmetric_difference(set_tokens2)

    return len(diff_tokens)


def swap_char(word):
    """Swap char."""
    chars = list(word)
    max_char = 4
    if len(chars) <= max_char:
        chars[1], chars[2] = chars[2], chars[1]
        return "".join(chars)

    lower = 1
    upper = len(chars) - 1

    pos1, pos2 = random.sample(range(lower, upper), 2)
    if pos1 + 1 < upper and pos1 + 1 != pos2:
        chars[pos1], chars[pos1 + 1] = chars[pos1 + 1], chars[pos1]

    if pos2 + 1 < upper and pos2 + 1 != pos1:
        chars[pos2], chars[pos2 + 1] = chars[pos2 + 1], chars[pos2]
    return "".join(chars)
