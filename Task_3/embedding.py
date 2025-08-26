import os

import gensim
import gensim.downloader as api
import numpy as np
import pandas as pd
from tqdm import tqdm


def get_word_vector(model: gensim.models.KeyedVectors, word: str):
    """Obtain the vector representation of a word from the model.

    Parameters
    ----------
    model : gensim.models.KeyedVectors
        The word embeddings model.
    word : str
        The word to get the vector for.

    Returns
    -------
    np.ndarray
        The vector representation of the word.
    """
    return model[word]


def load_model(model: str = "fasttext-wiki-news-subwords-300") -> gensim.models.KeyedVectors:
    """Load a word embeddings model.

    Parameters
    ----------
    model : str, optional
        The name of the model to load, by default "fasttext-wiki-news-subwords-300"

    Returns
    -------
    gensim.models.KeyedVectors
        The loaded word embeddings model.
    """
    # Check if model is already downloaded
    model_path = os.path.join(api.BASE_DIR, model)

    if os.path.exists(model_path):
        print(f"Model '{model}' found in cache. Loading from: {model_path}")
    else:
        print(f"Model '{model}' not found in cache. Downloading...")
        print("This may take several minutes depending on your internet connection.")

    print(f"Loading model: {model}...")
    model_obj = api.load(model)
    print("Model loaded successfully!")
    return model_obj  # type: ignore


def create_sentence_embeddings(
    preprocessed_texts: pd.Series, model: gensim.models.KeyedVectors, method: str = "average"
) -> np.ndarray:
    """Create embeddings for a series of preprocessed texts.

    Parameters
    ----------
    preprocessed_texts : pd.Series
        Series with preprocessed texts (preprocessed_content_for_embedding column)
    model : gensim.models.KeyedVectors
        Pre-loaded embeddings model

    Returns
    -------
    np.ndarray
        2D array where each row is the average embedding of a sentence
    """
    if method not in ["average", "additive"]:
        raise ValueError(f"Invalid method: {method}. Choose 'average' or 'additive'.")

    # Obtain model dimensions
    try:
        vector_dim = model.vector_size  # type: ignore
    except AttributeError:
        # For some models, it may be vector_size or another property
        vector_dim = len(model.get_vector(list(model.key_to_index.keys())[0]))  # type: ignore

    # List to store embeddings (average or sum)
    sentence_embeddings = []

    print(f"Processing {len(preprocessed_texts)} documents...")
    for text in tqdm(
        preprocessed_texts, total=len(preprocessed_texts), desc="Processing documents..."
    ):
        words = text.split()

        word_embeddings = []

        # Obtain embedding for each word that exists in the model.
        for word in words:
            try:
                embedding = get_word_vector(model, word)
                word_embeddings.append(embedding)
            except KeyError:
                # If the word is not found (OOV), use zero vector
                embedding = np.zeros(model.vector_size)
                word_embeddings.append(embedding)

        # Initialize sent_embeddings with a default value
        sent_embeddings = np.zeros(vector_dim)

        # Calculate the sentence embedding
        if word_embeddings:
            word_embeddings_array = np.array(word_embeddings)
            if method == "average":
                sent_embeddings = np.mean(word_embeddings_array, axis=0)
            elif method == "additive":
                sent_embeddings = np.sum(word_embeddings_array, axis=0)

        sentence_embeddings.append(sent_embeddings)

    return np.array(sentence_embeddings)


def save_embeddings(embeddings: np.ndarray, filepath: str) -> None:
    """Save embeddings to a file.

    Parameters
    ----------
    embeddings : np.ndarray
        2D array with embeddings to save
    filepath : str, optional
        Path to save the file, by default "data/ESM"
    """
    # Create directory if it does not exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Save embeddings
    np.savez_compressed(f"{filepath}.npz", embeddings=embeddings)
    print(f"Embeddings saved at: {filepath}")


def load_embeddings(filepath: str):
    """Load embeddings from a .npz file.

    Parameters
    ----------
    filepath : str
        Path to the file containing the embeddings

    Returns
    -------
    np.ndarray
        Array with the loaded embeddings
    """
    data = np.load(filepath)
    return data["embeddings"]


if __name__ == "__main__":
    texts = pd.Series(
        [
            "This is a sample document.",
            "This document is another sample.",
            "And this is a third one.",
        ]
    )

    model = load_model()

    # Example usage
    sem_average = create_sentence_embeddings(texts, model, method="average")
    sem_additive = create_sentence_embeddings(texts, model, method="additive")

    print("Semantic Average Vectors:")
    print(sem_average)
    print("Semantic Average shape:", sem_average.shape)

    print("\nSemantic Additive Vectors:")
    print(sem_additive)
    print("Semantic Additive shape:", sem_additive.shape)
