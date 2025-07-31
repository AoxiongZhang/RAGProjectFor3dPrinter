from utils import *

import os
from glob import glob
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader, PyMuPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def doc2vec():
    # spliter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 50
    )

    # read and embedding
    dir_path = os.path.join(os.path.dirname(__file__), './data/inputs/')

    documents = []
    for file_path in glob(dir_path + '*.*'):
        loader = None
        if file_path.endswith('.csv'):
            loader = CSVLoader(file_path, encoding="utf-8")
        elif file_path.endswith('.pdf'):
            loader = PyMuPDFLoader(file_path)
        elif file_path.endswith('.txt') or file_path.endswith('.md'):
            loader = TextLoader(file_path, encoding="utf-8")

        if loader:
            documents += loader.load_and_split(text_splitter)
#    print(documents)
            
    # vectorizing and store
    if documents:
        vdb = Chroma.from_documents(
            documents = documents, 
            embedding = get_embeddings_model(),
            persist_directory = os.path.join(os.path.dirname(__file__), './data/db/')
        )



if __name__ == '__main__':
    doc2vec()