from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def build_rag_chain():
    # STEP 1: load documents
    loader = DirectoryLoader(
        "./bank_docs/",
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} documents")

    # STEP 2: split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    # STEP 3: embed and store
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    print("Vectorstore ready")

    # STEP 4: build chain
    prompt = PromptTemplate.from_template("""
You are a helpful banking operations assistant.
Use ONLY the following context to answer the question.
If the answer is not in the context, say "I don't have that information."

Context:
{context}

Question: {question}

Answer:""")

    llm = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        temperature=0
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever


def ask(chain, retriever, question: str):
    answer = chain.invoke(question)
    docs = retriever.invoke(question)
    print(f"\nQ: {question}")
    print(f"A: {answer}")
    print("Sources:")
    for doc in docs:
        print(f"  - {doc.metadata.get('source', 'unknown')}")

def ask_policy_question(question: str) -> str:
    chain, retriever = build_rag_chain()
    answer = chain.invoke(question)
    return answer

if __name__ == "__main__":
    chain, retriever = build_rag_chain()
    ask(chain, retriever, "What is the maximum wire transfer limit for personal accounts?")
    ask(chain, retriever, "What documents are needed for a loan application?")
    ask(chain, retriever, "What is the overdraft fee?")