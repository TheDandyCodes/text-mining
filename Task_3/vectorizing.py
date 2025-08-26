import json
from typing import Iterable, Union

import pandas as pd
from scipy import sparse
from scipy.sparse._csr import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def vectorize_text(
    text: Union[list[str], pd.Series, Iterable[str]], method: str = "bow"
) -> tuple[csr_matrix, dict[str, int]]:
    """Vectorize text using different methods.

    Parameters
    ----------
    text : Union[list[str], pd.Series, Iterable[str]]
        The text to vectorize, can be a list of strings, a pandas Series, or any iterable of strings.
    method : str, optional
        The vectorization method to use, by default "bow"

    Returns
    -------
    tuple[csr_matrix, list[str]]
        The vectorized sparse matrix representation of the text.
    """
    if method == "bow":
        # Create the CountVectorizer object
        vectorizer = CountVectorizer()
    elif method == "tfidf":
        # Create the TfidfVectorizer object
        vectorizer = TfidfVectorizer()
    else:
        raise ValueError(
            f"Unsupported vectorization method: {method}. Available methods are: 'bow', 'tfidf'."
        )

    # Fit and transform the texts to obtain the count matrix
    X = vectorizer.fit_transform(text)

    # Vocabulary
    vocab = vectorizer.vocabulary_

    return X, vocab


def save_vectors_scipy(vectors: csr_matrix, vocab: dict[str, int], filepath: str):
    """Save vectorized text data in SciPy format.

    Parameters
    ----------
    vectors : csr_matrix
        The sparse matrix representation of the vectorized text.
    vocab : dict[str, int]
        The vocabulary mapping of words to their feature indices.
    filepath : str
        The file path to save the vectorized data.
    """
    import os

    # Create directories if they do not exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Save sparse matrices
    sparse.save_npz(f"{filepath}.npz", vectors)

    # Save vocabularies as JSON or pickle
    with open(f"{filepath}_vocab.json", "w") as f:
        json.dump(vocab, f)

    print(f"Sparse matrices saved to {filepath}.npz")


def load_vectors_scipy(filepath: str):
    """Load vectorized text data from SciPy format.

    Parameters
    ----------
    filepath : str
        The file path to load the vectorized data.

    Returns
    -------
    tuple[csr_matrix, dict[str, int]]
        The vectorized sparse matrix representation of the text and the vocabulary mapping.
    """
    import json

    # Load matrices
    vectors = sparse.load_npz(f"{filepath}.npz")

    # Load vocabularies
    with open(f"{filepath}_vocab.json") as f:
        vocab = json.load(f)

    return vectors, vocab


if __name__ == "__main__":
    texts = [
        "This is a sample document.",
        "This document is another sample.",
        "And this is a third one.",
    ]

    # Example usage
    bow_vectors, bow_vocab = vectorize_text(texts, method="bow")
    tfidf_vectors, tfidf_vocab = vectorize_text(texts, method="tfidf")

    print("Bag of Words Vectors:")
    print(bow_vectors)
    print("BoW shape:", bow_vectors.shape)

    print("\nTF-IDF Vectors:")
    print(tfidf_vectors)
    print("TF-IDF shape:", tfidf_vectors.shape)
