import re


def clean_text(text: str) -> str:
    text = re.sub(r"[^\w\s.,;:?!-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def batch_generator(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]
