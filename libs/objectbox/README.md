# langchain-objectbox

## About

This package contains the [ObjectBox](https://objectbox.io) integrations for [LangChain](https://www.langchain.com).

## Getting Started 

Install the `langchain-objectbox` package from PyPI via pip.

```
pip install langchain-objectbox
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

### Example 2: A more complex example using web retrieval chain.

Prerequisites: 

- Ollama as local LLM: See installation notes on https://python.langchain.com/docs/get_started/quickstart
- ``pip install langchain bs4``

```python
from langchain_objectbox.vectorstores import ObjectBox

from langchain_community.llms import Ollama
llm = Ollama(model="llama2")

from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")

docs = loader.load()

from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings()

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts.chat import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)

vector = ObjectBox.from_documents(documents, embeddings, embedding_dimensions=768)
document_chain = create_stuff_documents_chain(llm, prompt)
from langchain_core.documents import Document
from langchain.chains import create_retrieval_chain

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "how can langsmith help with testing?"})
print(response["answer"])
```

## LICENSE

```
MIT License

Copyright (c) 2024 ObjectBox, Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
