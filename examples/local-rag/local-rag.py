from langchain_community.llms import Ollama
from langchain_objectbox.vectorstores import ObjectBox

llm = Ollama(model="phi3")
from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="znbang/bge:small-en-v1.5-f32")  # 134 MB, 384 dim, (12 docs: 1.1s)
embeddings_dim = 384

print("Let's go...")
embedding_vector = embeddings.embed_query("How to create a ObjectBox query in Java?")
print("Embedding query vector:", len(embedding_vector))
print(embedding_vector[:10])

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts.chat import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

docs = []
from langchain_community.document_loaders import TextLoader

docs.extend(TextLoader("objectbox_data.txt").load())
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
documents = text_splitter.split_documents(docs)
print("Documents splitted: ", len(documents))

objectbox = ObjectBox.from_documents(documents, embeddings, embedding_dimensions=embeddings_dim, do_log=True,
                                     clear_db=True)

# These 2 lines are not part of the document chain but show how to use ObjectBox more directly (and print the results)
results = objectbox.similarity_search_by_vector(embedding_vector, 2)
print(results)

print("Generating result...")

document_chain = create_stuff_documents_chain(llm, prompt)
from langchain.chains import create_retrieval_chain

retriever = objectbox.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke(
    {
        "input": "How to create a ObjectBox query in Java, e.g. for an existing entity Person? "
                 "Search by address Sesame Street 1"})
print(response["answer"])

# Note: the quality of the answer is not great, but given that we feed it only with a few lines of input, it's not bad.
#       The more information you can provide, the better the answer will be.
