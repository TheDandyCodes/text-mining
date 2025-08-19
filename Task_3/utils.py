from pathlib import Path

import pandas as pd


def build_corpus_dataframe(corpus_path: str) -> pd.DataFrame:
    """
    Build a DataFrame where each row represents a document from the corpus.

    Parameters
    ----------
    corpus_path : str
        Path to the corpus directory

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['category', 'document_id', 'content', 'file_path']
    """
    data = []

    # Get the corpus directory
    corpus_dir = Path(corpus_path)

    # Iterate through each category folder
    for category_folder in corpus_dir.iterdir():
        if category_folder.is_dir() and not category_folder.name.startswith("."):
            category = category_folder.name
            # print(f"Processing category: {category}")

            # Iterate through each document in the category
            for doc_file in category_folder.iterdir():
                if doc_file.is_file() and not doc_file.name.startswith("."):
                    try:
                        # Read the document content
                        with open(doc_file, encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                        # Add document data to list
                        data.append(
                            {
                                "category": category,
                                "document_id": doc_file.name,
                                "content": content,
                            }
                        )

                    except Exception as e:
                        print(f"Error reading file {doc_file}: {e}")

    # Create DataFrame
    df = pd.DataFrame(data)
    return df
