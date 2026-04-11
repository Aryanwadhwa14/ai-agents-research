from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from typing import List

def create_chunks(documents: List[Document], chunk_size: int = 512, chunk_overlap: int = 50) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(documents)
