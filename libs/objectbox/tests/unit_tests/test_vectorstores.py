from langchain_core.embeddings.fake import (
    FakeEmbeddings,
)

from langchain_objectbox.vectorstores import ObjectBox


def test_initialization() -> None:
    """Test integration vectorstore initialization."""
    texts = ["foo", "bar", "baz"]
    ObjectBox.from_texts(
        # collection_name="test_collection",
        texts=texts,
        embedding=FakeEmbeddings(size=10),
        embedding_dimensions=768
    )
