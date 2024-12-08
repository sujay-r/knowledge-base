from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk(text: str) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, length_function=len
    )
    splits = text_splitter.split_text(text)
    return splits
