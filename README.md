# langchain-objectbox

## About

This package contains the [ObjectBox](https://objectbox.io) integrations for [LangChain](https://www.langchain.com).

## Getting Started 

Install the `langchain-objectbox` package from PyPI via pip.

```
pip install --pre langchain-objectbox
```

In Python import the ObjectBox vector store which is available under fully qualified class path `langchain_objectbox.vectorstores.ObjectBox`, e.g.:

```
from langchain_objectbox.vectorstores import ObjectBox
```

Create an ObjectBox VectorStore using e.g. one of the `from_` class methods e.g. `from_texts` class method.

**NOTE:** Ensure to set argument `embedding_dimensions` along with the dimensions used in your embeddings model.

```
obx_vectorstore = ObjectBox.from_texts(texts, embeddings, embedding_dimensions=768)
```

### Example 1: A *very* simple example using DeterministicFakeEmbedding

```python
from langchain_core.embeddings.fake import DeterministicFakeEmbedding
from langchain_objectbox.vectorstores import ObjectBox

texts = ["foo", "bar", "baz"]
obx_vectorstore = ObjectBox.from_texts(
    texts, 
    DeterministicFakeEmbedding(size=10),
    embedding_dimensions=10,
)
result = obx_vectorstore.similarity_search("foo",k=1)
print(result)
```
