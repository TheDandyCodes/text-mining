import re


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
            # Look for the end of header (empty line after "Lines:" field)
            if line.strip() == "" and i > 0:
                # Check if previous lines contain typical header fields
                prev_lines = lines[max(0, i - 5) : i]
                has_header_fields = any(
                    line.strip().startswith(
                        (
                            "From:",
                            "Subject:",
                            "Date:",
                            "Message-ID:",
                            "Lines:",
                            "Organization:",
                            "Newsgroups:",
                        )
                    )
                    for line in prev_lines
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


if __name__ == "__main__":
    import pandas as pd

    corpus_raw_df = pd.read_csv("data/corpus_raw.csv")
    corpus_raw_df["cleaned_content"] = (
        corpus_raw_df["content"].apply(clean_header).apply(remove_writes_lines)
    )
    print(corpus_raw_df.head())
