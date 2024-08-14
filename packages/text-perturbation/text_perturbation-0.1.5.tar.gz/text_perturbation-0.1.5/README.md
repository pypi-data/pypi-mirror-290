### Text Perturbation

This project is about the NLP task for text perturbation using different perturbation methods.
There are around 11 different methods.

1. delete_random_word : deletes randomly words
2. replace_synonyms : replaces a word with a synonym
3. backtranslation: translates english to german and back to english
4. paraphrase_using_bart: paraphrase the sentence
5. replace_with_hypernyms: replaces a word with hypernym
6. random_german_word: replace random word with a german word
7. predict_masked_word: masks a word from the sentence, then predicts using MLM
8. misspelling: simple typoes
9. random_char_insertion: randomly inserion character in a word
10. random_char_swaps: swaps character in a word
11. ocr_augmentation: augment word same as ocr.

Example to text perturbation:
```bash
# Example
from text_perturbation import perturbation
text = "hello, how are you?"

perturbate = perturbation.Perturbate(text)
perturbated_text = perturbate.random_german_word()

print(f"originial::: {text}")
print(f"perturbated_text::: {perturbated_text}")
```


Note: Please ensure the nltk data is downloaded. If not, use the following code to download.

```bash
# Example installation command
>>> import nltk
>>> nltk.download()



