import os
import shutil
from typing import Generator

import pytest

from langchain_objectbox.vectorstores import ObjectBox
from langchain.retrievers import ParentDocumentRetriever
from langchain.retrievers.multi_vector import MultiVectorRetriever
from tests.integration_tests.vectorstores.fake_embeddings import FakeEmbeddings
from langchain.storage import InMemoryStore, InMemoryByteStore
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

from objectbox.c import obx_remove_db_files, c_str

def remove_test_dir(test_dir: str) -> None:
    obx_remove_db_files(c_str(test_dir)) 

@pytest.fixture(autouse=True)
def auto_cleanup() -> Generator[None, None, None]:
    remove_test_dir("data")
    try:
        yield  # run the test function
    finally:
        remove_test_dir("data")


def test_objectbox_db_initialisation() -> None:
    ObjectBox(embedding=FakeEmbeddings(), embedding_dimensions=10)
    folder_path = "data"

    assert os.path.exists(folder_path), f"Folder '{folder_path}' does not exist."

    filepath = os.path.join(folder_path, "data.mdb")
    assert os.path.isfile(
        filepath
    ), f"File '{folder_path}' not found in '{folder_path}'"


def test_similarity_search() -> None:
    ob = ObjectBox(embedding=FakeEmbeddings(), embedding_dimensions=10)
    texts = ["foo", "bar", "baz"]
    ob.add_texts(texts=texts)

    query = ob.similarity_search("foo", k=1)
    assert len(query) == 1

    query = ob.similarity_search("foo", k=2)
    assert len(query) == 2

    query = ob.similarity_search("foo", k=3)
    assert len(query) == 3


def test_from_texts() -> None:
    texts = ["foo", "bar", "baz"]
    ob = ObjectBox.from_texts(
        embedding=FakeEmbeddings(), embedding_dimensions=10, texts=texts
    )

    # positive test
    query = ob.similarity_search("foo", k=2)
    assert len(query) == 2


def test_similarity_search_with_score() -> None:
    ob = ObjectBox(embedding=FakeEmbeddings(), embedding_dimensions=10)
    texts = ["foo", "bar", "baz"]
    ob.add_texts(texts=texts)

    query = ob.similarity_search_with_score("foo", k=1)
    assert len(query) == 1

    query = ob.similarity_search_with_score("foo", k=2)
    assert len(query) == 2

    query = ob.similarity_search_with_score("foo", k=3)
    assert len(query) == 3


def test_similarity_search_by_vector() -> None:
    ob = ObjectBox(embedding=FakeEmbeddings(), embedding_dimensions=10)
    texts = ["foo", "bar", "baz"]
    ob.add_texts(texts=texts)

    query_embedding = FakeEmbeddings().embed_query("foo")
    query = ob.similarity_search_by_vector(query_embedding, k=1)
    assert len(query) == 1

    query = ob.similarity_search_by_vector(query_embedding, k=2)
    assert len(query) == 2

    query = ob.similarity_search_by_vector(query_embedding, k=3)
    assert len(query) == 3


def test_delete_vector_by_ids() -> None:
    ob = ObjectBox(embedding=FakeEmbeddings(), embedding_dimensions=10)
    texts = ["foo", "bar", "baz"]
    ob.add_texts(texts=texts)

    bool = ob.delete(["1", "2"])
    assert bool is True

    assert ob._vector_box.count() == 1


def OFF_test_parent_document_retriever() -> None:
    loaders = [
        TextLoader("testdata/paul_graham_essay.txt"),
        TextLoader("testdata/state_of_the_union.txt"),
    ]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())

    # This text splitter is used to create the child documents
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
    # The vectorstore to use to index the child chunks
    vectorstore = ObjectBox(
        embedding=HuggingFaceEmbeddings(), embedding_dimensions=768,
    )
    # The storage layer for the parent documents
    store = InMemoryStore()
    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        id_key="id",
    )

    retriever.add_documents(docs, ids=None)

    assert len(list(store.yield_keys())) == 2

    sub_docs = vectorstore.similarity_search("justice breyer")

    retrieved_docs = retriever.invoke("justice breyer")
    assert len(retrieved_docs[0].page_content) == 38540


def OFF_test_multi_vector_retriever() -> None:
    loaders = [
        TextLoader("testdata/paul_graham_essay.txt"),
        TextLoader("testdata/state_of_the_union.txt"),
    ]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000)
    docs = text_splitter.split_documents(docs)
    # The vectorstore to use to index the child chunks
    vectorstore = ObjectBox(
        embedding=HuggingFaceEmbeddings(), embedding_dimensions=768
    )
    # The storage layer for the parent documents
    store = InMemoryByteStore()
    id_key = "id"
    # The retriever (empty to start)
    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        byte_store=store,
        id_key=id_key,
    )
    import uuid

    doc_ids = [str(uuid.uuid4()) for _ in docs]
    # The splitter to use to create smaller chunks
    child_text_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
    sub_docs = []
    for i, doc in enumerate(docs):
        _id = doc_ids[i]
        _sub_docs = child_text_splitter.split_documents([doc])
        for _doc in _sub_docs:
            _doc.metadata[id_key] = _id
        sub_docs.extend(_sub_docs)

    retriever.vectorstore.add_documents(sub_docs)
    retriever.docstore.mset(list(zip(doc_ids, docs)))

    # Vectorstore alone retrieves the small chunks
    res = retriever.vectorstore.similarity_search("justice breyer")[0]

    # Retriever returns larger chunks
    assert len(retriever.invoke("justice breyer")[0].page_content) == 9875

    docs = text_splitter.split_documents(docs)
