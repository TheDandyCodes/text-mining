# spacy_pos.py
from typing import Literal

import spacy
from spacy.tokens import Doc


# If not installed: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")  # 3.x/4.x


def spacy_pos(
    tokenized_text: list[list[str]], tagging: Literal["PTB", "UPOS"] = "PTB"
) -> list[list[tuple[str, str]]]:
    """
    Returns per sentence: [(token, UPOS=token.pos_, PTB=token.tag_), ...]
    Uses pos_ for Universal POS; uses tag_ for Penn Treebank (comparable to Stanford).

    Args:
        tokenized_text: List of sentences, each as a list of tokens
        tagging: Either "PTB" for Penn Treebank tags or "UPOS" for Universal POS tags
    """
    results = []

    for sentence_tokens in tokenized_text:
        # Create a spaCy Doc from pre-tokenized text to avoid re-tokenization
        # This ensures we use exactly the same tokens as NLTK/Stanford
        spaces = [True] * len(sentence_tokens)  # Assume spaces between all tokens
        if len(spaces) > 0:
            spaces[-1] = False  # No space after last token

        doc = Doc(nlp.vocab, words=sentence_tokens, spaces=spaces)

        # Process the doc through the pipeline (but skip tokenizer since we already have tokens)
        for pipe_name, pipe_component in nlp.pipeline:
            if pipe_name != "tokenizer":  # Skip tokenizer
                doc = pipe_component(doc)

        # Extract tags for each token
        sentence_tags = []
        for i, token in enumerate(doc):
            if tagging == "PTB":
                tag = token.tag_
            elif tagging == "UPOS":
                tag = token.pos_
            else:
                raise ValueError(f"Unknown tagging type: {tagging}. Must be 'PTB' or 'UPOS'.")

            sentence_tags.append((sentence_tokens[i], tag))

        results.append(sentence_tags)

    return results


if __name__ == "__main__":
    import nltk

    sample = "Time flies like an arrow; fruit flies like a banana. The old man the boats."

    # Tokenize the sample text like stanford_pos expects
    sents = nltk.sent_tokenize(sample)
    tokenized_sample = [nltk.word_tokenize(s) for s in sents]

    for i, sent in enumerate(spacy_pos(tokenized_sample)):
        print(f"Sentence {i + 1}:")
        print(sent)
