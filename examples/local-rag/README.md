# Example: Local RAG using langchain-objectbox with ollama models

## Setup

 1. Install ollama. See instructions at https://ollama.com/download

 2. Pull models

        ollama pull phi3
        ollama pull znbang/bge:small-en-v1.5-f32
 
 3. Change to this directory:

        cd examples/local-rag

 4. Recommended: Create a new venv

        python3 -m venv .venv
        source .venv/bin/activate

 5. Install `langchain-objectbox` and `langchain`: 

        pip install langchain-objectbox
        pip install langchain
    Or: 

        pip install -r requirements.txt

For your convenience, you can run `setup.sh` for Step 2 and 5.

## Run Example
        
~~~
$ python local-rag.py 

Let's go...
Embedding query vector: 384
[-0.7788800001144409, 0.18136192858219147, -0.1711404025554657, -0.1458890736103058, -0.3066989481449127, -0.181111142039299, 0.14091172814369202, 0.2811528444290161, -0.29055193066596985, 0.7156291604042053]
Documents splitted:  12
Embedded  12 documents in 1.7314591539980029 seconds
ObjectBox stored 12 documents in 0.02562471900091623 seconds
ObjectBox ready
ObjectBox retrieved 2 vectors in 0.0016720460007491056 seconds
[Document(page_content='ObjectBox Query example (Java):\n```java\nQuery<User> query = userBox.query(User_.firstName.equal("Joe")).build();\nList<User> joes = query.find();\nquery.close();\n```\n\nObjectBox Query example (Kotlin):\n```kotlin\nval query = userBox.query(User_.firstName.equal("Joe")).build()\nval joes = query.find()\nquery.close()\n```', metadata={'source': 'objectbox_data.txt'}), Document(page_content='ObjectBox Query example (Kotlin):\n```kotlin\nval query = userBox.query(User_.firstName.equal("Joe")).build()\nval joes = query.find()\nquery.close()\n```\n\nFor example to get users with the first name “Joe” that are born later than 1970 and whose last name starts with “O”:', metadata={'source': 'objectbox_data.txt'})]
ObjectBox retrieved 4 vectors in 0.00039298100091400556 seconds
To create a Query object using ObjectBox's Query API in Kotlin for an existing `Person` entity and search by the address "Sesamestreet 1", you can use the following code:

```kotlin
val query = personBox.query().where(Person::address).equal("Sesamestreet 1").build()
val people = query.find()
query.close()
```

In this example, `personBox` is an instance of a BoxStore for the `Person` entity and `Person::address` represents accessing the address property within the `Person` class using Kotlin's property access syntax.
~~~

