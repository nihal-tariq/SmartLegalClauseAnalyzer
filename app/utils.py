import re


def clean_text(text: str) -> str:
    """
    Cleans the input text by removing unwanted characters and extra spaces.

    Removes all characters except word characters, spaces, and basic punctuation
    (.,;:?!-). Also collapses multiple spaces into a single space and strips leading/trailing whitespace.

    Args:
        text (str): The input text to clean.

    Returns:
        str: The cleaned text.
    """
    text = re.sub(r"[^\w\s.,;:?!-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def batch_generator(data, batch_size):
    """
    Generates batches of data from a list or sequence.

    Splits the input data into chunks (batches) of the specified batch size,
    yielding one batch at a time.

    Args:
        data (list or sequence): The data to be split into batches.
        batch_size (int): The number of items in each batch.

    Yields:
        list: A batch of data with length <= batch_size.
    """
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]
