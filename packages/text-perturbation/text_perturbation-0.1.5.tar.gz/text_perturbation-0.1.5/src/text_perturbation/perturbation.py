"""perturbate file."""

import random
import secrets
import string

import nlpaug.augmenter.char as nac
import nlpaug.augmenter.word as naw
import nltk
from nltk.tokenize import word_tokenize
from transformers import M2M100ForConditionalGeneration
from transformers import M2M100Tokenizer
from transformers import pipeline

from .helper import detokenize
from .helper import device
from .helper import get_hypernyms
from .helper import get_synonyms
from .helper import remove_punctuations
from .helper import remove_stopwords
from .helper import swap_char



class Perturbate:
    """perturbate class."""

    def __init__(self, sentence):
        """Initilize class.

        Attrs:
            param: sentence(str): input sentence to be perturbated
        """
        self.sentence = sentence
        self.perturbation_functions = {
            "delete_random_word": self.delete_random_word,
            "replace_synonyms": self.replace_synonyms,
            "backtranslation": self.backtranslation,
            "paraphrase_using_bart": self.paraphrase_using_bart,
            "replace_with_hypernyms": self.replace_with_hypernyms,
            "random_german_word": self.random_german_word,
            "predict_masked_word": self.predict_masked_word,
            "misspelling": self.misspelling,
            "random_char_insertion": self.random_char_insertion,
            "random_char_swaps": self.random_char_swaps,
            "ocr_augmentation": self.ocr_augmentation,
        }

    def misspelling(self):
        """Spelling mistake."""
        aug = naw.SpellingAug()
        augmented_texts = aug.augment(self.sentence, n=1)
        return augmented_texts[0]

    def delete_random_word(self, level=2):
        """Delete random word.

        Attrs:
            param: level (int): indicates the intensity of deletion
        """
        sentence_copy = word_tokenize(self.sentence)
        text_no_punctuation = remove_punctuations(self.sentence)
        words_no_stopwords = remove_stopwords(text_no_punctuation)

        length = len(sentence_copy)
        max_length = 10
        levels = {"level_1": 1, "level_2": 2}
        if length < max_length:
            num_of_words = 1
        elif level == levels["level_1"]:
            num_of_words = int(length * 0.1)
        elif level == levels["level_2"]:
            num_of_words = int(length * 0.2)
        else:
            num_of_words = int(length * 0.3)

        tokens_to_delete = random.sample(words_no_stopwords, num_of_words)
        remaining_words = [
            word for word in sentence_copy if word not in tokens_to_delete
        ]

        return detokenize(remaining_words)

    def replace_synonyms(self):
        """Replace synonyms."""
        num_to_replace = 2
        sentence_copy = word_tokenize(self.sentence).copy()

        text_no_punctuation = remove_punctuations(self.sentence)
        random_word_list = remove_stopwords(text_no_punctuation)

        random.shuffle(random_word_list)
        num_replaced = 0

        for random_word in random_word_list:
            synonyms = get_synonyms(random_word)

            if len(synonyms) >= 1:
                synonym = random.SystemRandom().choice(synonyms)
                sentence_copy = [
                    synonym if word == random_word else word
                    for word in sentence_copy
                ]
                num_replaced += 1

            if num_replaced >= num_to_replace:  # only replace up to n words
                break

        return detokenize(sentence_copy)

    def backtranslation(self):
        """Backtranslation method.

        model: "facebook/m2m100_418M"
        source: https://huggingface.co/facebook/m2m100_418M
        """
        tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
        model = M2M100ForConditionalGeneration.from_pretrained(
            "facebook/m2m100_418M"
        )
        model.to(device)

        # English to German
        tokenizer.src_lang = "en"
        tokenizer.tgt_lang = "de"

        encoded = tokenizer(self.sentence, return_tensors="pt")
        translated_tokens = model.generate(
            **encoded, forced_bos_token_id=tokenizer.get_lang_id("de")
        )
        de_text = tokenizer.decode(
            translated_tokens[0], skip_special_tokens=True
        )

        # German to English
        tokenizer.src_lang = "de"
        tokenizer.tgt_lang = "en"

        encoded = tokenizer(de_text, return_tensors="pt")
        translated_tokens = model.generate(
            **encoded, forced_bos_token_id=tokenizer.get_lang_id("en")
        )
        return tokenizer.decode(translated_tokens[0], skip_special_tokens=True)


    def paraphrase_using_bart(self):
        """Paraphrase using open source Bart model from hugging face.

        model: "eugenesiow/bart-paraphrase"
        source: https://huggingface.co/eugenesiow/bart-paraphrase
        """
        pipe = pipeline(
            "text2text-generation",
            model="eugenesiow/bart-paraphrase",
            device=device,
        )

        generations = pipe(self.sentence)
        paraphrased_sentence = generations[0]["generated_text"]
    
        return paraphrased_sentence

    def replace_with_hypernyms(self):
        """Replace with hypernyms."""
        num_of_word = 2
        # tokenization
        sentence_tokenized = word_tokenize(self.sentence)
        sentence_copy = sentence_tokenized.copy()
        tagged_tokens = nltk.pos_tag(sentence_tokenized)
        random_word_list = [
            tag[0] for tag in tagged_tokens if tag[1] in {"NN", "NNS"}
        ]
        random.shuffle(random_word_list)
        num_replaced = 0
        for random_word in random_word_list:
            hypernym = get_hypernyms(random_word)
            if hypernym != random_word and len(hypernym) >= 1:
                sentence_copy = [
                    hypernym if word == random_word else word
                    for word in sentence_copy
                ]
                num_replaced += 1

                if num_replaced >= num_of_word:  # only replace up to 2 words
                    break
        return detokenize(sentence_copy)

    def random_german_word(self):
        """Change a random word to german.

        Model: facebook/m2m100_418M
        source: https://huggingface.co/facebook/m2m100_418M
        """
        sentence_without_punctuation = remove_punctuations(self.sentence)
        sentence_tokens = word_tokenize(self.sentence)
        sentence_copy = sentence_tokens.copy()

        sentence_without_stopwords = remove_stopwords(
            sentence_without_punctuation
        )

        random_word = random.SystemRandom().choice(sentence_without_stopwords)

        tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
        model = M2M100ForConditionalGeneration.from_pretrained(
            "facebook/m2m100_418M"
        )
        model.to(device)

        # English to German
        tokenizer.src_lang = "en"
        tokenizer.tgt_lang = "de"

        encoded = tokenizer(random_word, return_tensors="pt")
        translated_tokens = model.generate(
            **encoded, forced_bos_token_id=tokenizer.get_lang_id("de")
        )
        de_word = tokenizer.decode(
            translated_tokens[0], skip_special_tokens=True
        )

        sentence_copy = [
            de_word if word == random_word else word for word in sentence_copy
        ]
        return detokenize(sentence_copy)

    def predict_masked_word(self):
        """Predict a masked word."""
        mask = "[MASK]"

        without_punctuation = remove_punctuations(self.sentence)
        without_stopwords = remove_stopwords(without_punctuation)
        sentence_copy = word_tokenize(self.sentence)

        if not without_stopwords:
            return self.sentence

        random_word = random.SystemRandom().choice(without_stopwords)
        masked_sentence_tokens = [
            mask if word == random_word else word for word in sentence_copy
        ]
        masked_sentence = detokenize(masked_sentence_tokens)

        if mask in masked_sentence_tokens:
            unmasker = pipeline("fill-mask", model="bert-base-uncased")

            if unmasker(masked_sentence):
                for prediction in unmasker(masked_sentence):
                    if (
                        "token_str" in prediction
                        and prediction["token_str"] != random_word
                    ):
                        predicted_word = prediction["token_str"]
                        prediction_tokens = [
                            predicted_word if word == mask else word
                            for word in masked_sentence_tokens
                        ]

                        return detokenize(prediction_tokens)
            else:
                print(
                    "Unable to predict the masked word. Perturbation failed!!!"
                )
                return self.sentence
        else:
            print("Word not masked. Perturbation failed!!!")
        return self.sentence

    # New perturbation method.
    def random_char_insertion(self):
        """Random insertion of character."""
        chars_to_insert = list(string.ascii_lowercase + string.digits)

        orginal_sentence_tokens = word_tokenize(self.sentence)
        new_sentence = orginal_sentence_tokens.copy()
        sentence_without_punct = remove_punctuations(self.sentence)
        words = word_tokenize(sentence_without_punct)

        word_length = len(words)
        max_length_lower = 5
        max_length_upper = 8
        if word_length <= max_length_lower:
            num_of_words = 1
        elif word_length > max_length_lower and word_length < max_length_upper:
            num_of_words = int(word_length * 0.2)
        else:
            num_of_words = int(word_length * 0.4)

        random_words = random.sample(words, num_of_words)
        word_dict = {}
        max_char_length = 4
        for word in random_words:
            chars = list(word)
            num_char_to_insert = 1 if len(chars) < max_char_length else 2
            for _ in range(num_char_to_insert):
                position = secrets.randbelow(len(word))
                # Insert a random character at the chosen position
                random_char = secrets.choice(chars_to_insert)
                chars.insert(position, random_char)
            new_word = "".join(chars)
            word_dict[word] = new_word

        for key, value in word_dict.items():
            for idx, w in enumerate(new_sentence):
                if w == key:
                    new_sentence[idx] = value

        return detokenize(new_sentence)

    # New perturbation method
    def random_char_swaps(self):
        """Randomly swap two character."""
        sentence_tokens = word_tokenize(self.sentence)
        new_sentence = sentence_tokens.copy()

        sentence_with_pun = remove_punctuations(self.sentence)
        tokens = word_tokenize(sentence_with_pun)

        # Select the words with more than 4 characters
        max_char_length = 4
        min_char_length = 2
        tokens_with_more_chars = [
            word for word in tokens if len(word) > max_char_length
        ]

        if not tokens_with_more_chars:
            return self.sentence

        if len(tokens_with_more_chars) >= max_char_length:
            sample_size = 3
        elif len(tokens_with_more_chars) >= min_char_length:
            sample_size = 2
        else:
            sample_size = 1

        random_words = random.sample(tokens_with_more_chars, sample_size)

        word_dict = {}
        for word in random_words:
            new_word = swap_char(word)
            word_dict[word] = new_word
        for key, value in word_dict.items():
            for idx, w in enumerate(new_sentence):
                if w == key:
                    new_sentence[idx] = value
        return detokenize(new_sentence)

    # New Perturbation method.
    def ocr_augmentation(self):
        """OCR method augmentation."""
        aug = nac.OcrAug()
        perturbated_text = aug.augment(self.sentence, n=1)
        return perturbated_text[0]

    def call_by_type(self, perturbation_type):
        """Call perturabtion methods.

        Attrs:
            param: perturbation_type (str) : perturbation type
        """
        if perturbation_type in self.perturbation_functions:
            return self.perturbation_functions[perturbation_type]()

        print("function not found: ")
        return None
