import nltk
import sys

def ensure_nltk_data():
    try:
        # Check if 'punkt' tokenizer data is already available
        nltk.data.find('tokenizers/punkt')
        print("NLTK 'punkt' tokenizer is already installed.")
    except LookupError:
        # If 'punkt' data is not found, ask for permission to download
        print("NLTK 'punkt' tokenizer is missing.")
        user_input = input("Do you want to download the 'punkt' tokenizer data now? [y/N]: ").strip().lower()

        if user_input in ['y', 'yes']:
            print("Downloading NLTK 'punkt' tokenizer data...")
            nltk.download('punkt')
            print("Download complete.")
        else:
            print("You chose not to download the 'punkt' tokenizer data.")
            sys.exit("NLTK 'punkt' tokenizer data is required to proceed. Please download it manually.")

if __name__ == "__main__":
    ensure_nltk_data()
