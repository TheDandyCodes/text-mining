import re
from typing import Iterable, Union

import pandas as pd
import spacy
from tqdm import tqdm


def clean_header(content: str) -> str:
    """Remove newsgroup headers from the content.

    Parameters
    ----------
    content : str
        The raw newsgroup content.

    Returns
    -------
    str
        The cleaned content without headers, starting from the first line after the header.
    """
    lines = content.split("\n")

    # Find the end of the header (empty line after "Lines:" field)
    content_start = 0
    in_header = True

    for i, line in enumerate(lines):
        if in_header:
            # Look for the end of header (empty line after header fields)
            if line.strip() == "" and i > 0:
                # Check if previous lines contain header fields (any word followed by colon)
                prev_lines = lines[max(0, i - 5) : i]
                has_header_fields = any(
                    re.match(r"^[A-Za-z][A-Za-z0-9\-_]*:", line.strip()) for line in prev_lines
                )
                if has_header_fields:
                    content_start = i + 1
                    in_header = False
                    break

    # Get content after header
    content_lines = lines[content_start:]

    # Join lines and clean up extra whitespace
    cleaned_content = "\n".join(content_lines)
    cleaned_content = re.sub(r"\n\s*\n\s*\n", "\n\n", cleaned_content)  # Remove excessive newlines

    return cleaned_content.strip()


def remove_writes_lines(content: str) -> str:
    """Remove lines containing 'writes:' from the content.

    Parameters
    ----------
    content : str
        The raw newsgroup content.

    Returns
    -------
    str
        The cleaned content without 'writes:' lines and leading empty lines.
    """
    lines = content.split("\n")
    cleaned_lines = [line for line in lines if not re.search(r"\S+.*writes:\s*$", line.strip())]
    # Remove leading empty lines
    while cleaned_lines and cleaned_lines[0].strip() == "":
        cleaned_lines.pop(0)
    return "\n".join(cleaned_lines)


def remove_firm(content: str) -> str:
    # TODO
    return ""


def preprocessing_pipeline(
    content: Union[list[str], pd.Series, Iterable[str]],
    model: str = "en_core_web_sm",
    lemmatize: bool = True,
    batch_size: int = 1000,
):
    """Preprocess the text content in batch or individual mode.

    Parameters
    ----------
    content : str or list of str
        The raw text content to preprocess. Can be a single string or a list of strings.
    model : str, optional
        The spaCy model to use for tokenization and lemmatization, by default "en_core_web_sm"
    lemmatize : bool, optional
        Whether to apply lemmatization to the tokens, by default True
    batch_size : int, optional
        Batch size for processing when content is a list, by default 1000

    Returns
    -------
    str or list of str
        The preprocessed text. Returns a string if input was a string,
        or a list of strings if input was a list.
    """
    # Carga el modelo de spaCy en inglés
    nlp = spacy.load(model)

    def process_tokens(doc):
        """Extract and filter tokens from a spaCy doc."""
        tokens = [
            token.lemma_.lower() if lemmatize else token.text.lower()
            for token in doc
            if not token.is_punct
            and not token.is_space
            and token.text.strip() != ""  # Exclude empty tokens or tokens consisting only of spaces
            and not re.match(
                r"^[\s\t\n\r]+$", token.text
            )  # Exclude tokens that are only whitespace
            and not re.match(
                r"^[^\w\s]+$", token.text
            )  # Exclude tokens that are only symbols (|, >, ^^^, etc.)
            and len(token.text.strip()) > 0  # Ensure there is real content
        ]
        return " ".join(tokens)

    # Handle single string input (backward compatibility)
    if isinstance(content, str):
        doc = nlp(content)
        return process_tokens(doc)

    # Handle batch processing for list input
    elif isinstance(content, (list, tuple, pd.Series)):
        # Use nlp.pipe for efficient batch processing
        processed_texts = []
        for doc in tqdm(
            nlp.pipe(content, batch_size=batch_size),
            total=len(content),
            desc="Processing documents...",
        ):
            processed_texts.append(process_tokens(doc))
        return processed_texts

    else:
        raise ValueError("Content must be either a string or a list/tuple of strings")


if __name__ == "__main__":
    import pandas as pd

    # Try to load the corpus data if it exists
    try:
        corpus_raw_df = pd.read_csv("Task_3/data/corpus_raw.csv")
        corpus_raw_df["cleaned_content"] = (
            corpus_raw_df["content"].apply(clean_header).apply(remove_writes_lines)
        )
        print("DataFrame info:")
        print(corpus_raw_df.head())
    except FileNotFoundError:
        print("corpus_raw.csv not found, continuing with examples...")

    # Example of individual text processing
    text = """
    Hi, I wanted to ask you something, if I may. I'm thinking of buying a television for $32.50, although it's €33.00 on Amazon.
    """
    print("Individual text processing:")
    print(preprocessing_pipeline(text))

    # Example of batch processing
    print("\nBatch processing example:")
    sample_texts = [
        "Hello world! How are you?",
        "This is a test document.",
        "Machine learning is fascinating!",
    ]
    batch_results = preprocessing_pipeline(sample_texts)
    for i, result in enumerate(batch_results):
        print(f"Text {i + 1}: {result}")
