# stanford_pos_nltk.py
import nltk


# Basic downloads (one time only)
nltk.download("punkt_tab")

# Compatibility with different NLTK versions
try:
    from nltk.tag import StanfordPOSTagger
except Exception:
    from nltk.tag.stanford import StanfordPOSTagger  # fallback for old NLTK versions

# 1) Paths to YOUR files:
STANFORD_JAR = (
    "stanford-postagger-full-2020-11-17/stanford-postagger-4.2.0.jar"  # or 'stanford-postagger.jar'
)
STANFORD_MODEL = "stanford-postagger-full-2020-11-17/models/english-left3words-distsim.tagger"
# (in some packages you also have 'english-bidirectional-distsim.tagger')

# 2) Build the tagger
tagger = StanfordPOSTagger(
    model_filename=STANFORD_MODEL,
    path_to_jar=STANFORD_JAR,
    encoding="utf8",  # important for Unicode
    # java_options='-Xmx2g'                 # adjust memory if needed
)


def tokenize_text_nltk(text: str) -> list[list[str]]:
    """Tokenizes the input text into sentences and words."""
    sents = nltk.sent_tokenize(text)
    tokenized = [nltk.word_tokenize(s) for s in sents]
    return tokenized


def stanford_pos(tokenized_text: list[list[str]]) -> list[list[tuple[str, str]]]:
    """Returns list of sentences, each as [(token, PTB_tag), ...]."""
    tagged_sents = list(tagger.tag_sents(tokenized_text))  # one call per block
    return tagged_sents


if __name__ == "__main__":
    sample = "Time flies like an arrow; fruit flies like a banana. The old man the boats."
    # Tokenize the raw text for both taggers
    tokenized_text = [[str(word) for word, _ in sent] for sent in sample]

    for i, sent in enumerate(stanford_pos(tokenized_text)):
        print(f"Sentence {i + 1}:")
        print(sent)
