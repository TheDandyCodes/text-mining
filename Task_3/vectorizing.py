from typing import Iterable, Union

import pandas as pd
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


if __name__ == "__main__":
    texts = [
        "This is a sample document.",
        "This document is another sample.",
        "And this is a third one.",
    ]

    # Example usage
    bow_vectors = vectorize_text(texts, method="bow")
    tfidf_vectors = vectorize_text(texts, method="tfidf")

    print("Bag of Words Vectors:")
    print(bow_vectors)

    print("\nTF-IDF Vectors:")
    print(tfidf_vectors)
