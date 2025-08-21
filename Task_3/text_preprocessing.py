import re

import spacy


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
    content: str, model: str = "en_core_web_sm", lemmatize: bool = True
) -> list[str]:
    # Carga el modelo de spaCy en inglés
    nlp = spacy.load(model)

    # Procesa el texto
    doc = nlp(content)

    # Filtra tokens que no sean stop words ni signos de puntuación
    tokens = [
        token.lemma_.lower() if lemmatize else token.text.lower()
        for token in doc
        if not token.is_punct
        and not token.is_space
        and token.text.strip() != ""  # Exclude empty tokens or tokens consisting only of spaces
        and not re.match(r"^[\s\t\n\r]+$", token.text)  # Exclude tokens that are only whitespace
        and not re.match(
            r"^[^\w\s]+$", token.text
        )  # Exclude tokens that are only symbols (|, >, ^^^, etc.)
        and len(token.text.strip()) > 0  # Ensure there is real content
    ]

    return tokens


if __name__ == "__main__":
    import pandas as pd

    corpus_raw_df = pd.read_csv("data/corpus_raw.csv")
    corpus_raw_df["cleaned_content"] = (
        corpus_raw_df["content"].apply(clean_header).apply(remove_writes_lines)
    )

    text = """
    Hola, queria consultarte algo, puedo? Estoy pensando en comprar una television por 32.50$ aunque en amazon está por 33,00€
    """
    print(preprocessing_pipeline(text))
    print(corpus_raw_df.head())
