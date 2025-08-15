from typing import TypedDict

import nltk
from nltk.corpus import treebank
from pos_spacy import spacy_pos
from standford_pos_nltk import stanford_pos


class POSMismatch(TypedDict):
    word1: str
    tag1: str
    word2: str
    tag2: str


# Check if treebank corpus is available, if not, download it
try:
    treebank.tagged_sents()
except LookupError:
    print("Downloading NLTK treebank corpus...")
    nltk.download("treebank")


def extract_tokens_from_gold(gold) -> list[list[str]]:
    """
    Extracts tokens from the gold standard data.
    """
    return [[str(word) for word, _ in sent] for sent in gold]


def extract_raw_text(gold):
    """
    Extracts raw text from the gold standard data.
    """
    result = []
    for sent in gold:
        sentence = ""
        for word, _ in sent:
            if word in [".", ","]:
                sentence = sentence.rstrip() + word + " "
            else:
                sentence += word + " "
        result.append(sentence.strip())
    return " ".join(result)


def compare_pos_taggers(pos_tag_output_1, pos_tag_output_2) -> list[POSMismatch]:
    """
    Compares the output of two POS taggers.
    """
    mismatches = []
    for sent1, sent2 in zip(pos_tag_output_1, pos_tag_output_2):
        for (word1, tag1), (word2, tag2) in zip(sent1, sent2):
            if tag1 != tag2:
                # print(f"Tag mismatch: {tag1} != {tag2}")
                mismatches.append({"word1": word1, "tag1": tag1, "word2": word2, "tag2": tag2})
    return mismatches


def accuracy(pos_tag_output, gold) -> float:
    """
    Computes the accuracy of a POS tagger's output compared to the gold standard.
    """
    correct = 0
    total = 0
    for sent, gold_sent in zip(pos_tag_output, gold):
        for (_word, tag), (_gold_word, gold_tag) in zip(sent, gold_sent):
            if tag == gold_tag:
                correct += 1
            total += 1
    return correct / total if total > 0 else 0.0


if __name__ == "__main__":
    gold = treebank.tagged_sents()  # POS PTB

    tokenized_text = extract_tokens_from_gold(gold[:3])

    pos_tag_output_st_nltk = stanford_pos(tokenized_text)
    pos_tag_output_spacy = spacy_pos(tokenized_text)
    mismatches = compare_pos_taggers(pos_tag_output_st_nltk, pos_tag_output_spacy)
    print("Mismatches between Stanford NLTK and spaCy POS taggers:")
    for mismatch in mismatches:
        print(
            f"Word: {mismatch['word1']}, Stanford NLTK Tag: {mismatch['tag1']}, spaCy Tag: {mismatch['tag2']}"
        )

    acc_st_nltk = accuracy(pos_tag_output_st_nltk, gold)
    acc_spacy = accuracy(pos_tag_output_spacy, gold)
    print(f"Accuracy (Stanford NLTK): {acc_st_nltk:.4f}")
    print(f"Accuracy (spaCy): {acc_spacy:.4f}")
