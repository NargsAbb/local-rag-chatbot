import os
import tempfile
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import shutil
from langchain_core.documents import Document
from embeddings import embedding_function
from langchain_chroma import Chroma

def calculate_chunk_ids(chunks):

    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks


def getting_file():
    uploaded_file = st.file_uploader("Upload Your File(PDF)", type=["pdf"])

    if uploaded_file is None:
        return False
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_file_path = tmp_file.name

        try:
            loader = PyPDFLoader(temp_file_path)
            documents = loader.load()

            for doc in documents:
                doc.metadata["source"] = uploaded_file.name

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_documents(documents)

            st.success(f"(Chunks): {len(chunks)}")

        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        # Load the existing database.
        db = Chroma(
            persist_directory="chroma", embedding_function=embedding_function()
        )

        chunks_with_ids = calculate_chunk_ids(chunks)

        existing_items = db.get(include=[]) 
        existing_ids = set(existing_items["ids"])

        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
    return True

def clear_database():
    if os.path.exists("chroma"):
        shutil.rmtree("chroma")
        return True
    return False
