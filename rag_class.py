class RAG:
    def __init__(self, embeddings = None, model = "gpt-5-nano"):
        import openai
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
          # Safe embedding initialization
        if embeddings is None:
            embeddings = OpenAIEmbeddings()
        self.embeddings = embeddings
       
        self.llm = ChatOpenAI(model = model)
        # client_openai = openai.OpenAI()
        self.documents = []
        self.db = None
        self.retrieved_context =''

    def load_langchain_documents(self, path):
        import json
        from langchain_core.documents import Document
        with open(path, "r") as f:
            for line in f:
                raw = json.loads(line)
                self.documents.append(
                    Document(
                        page_content=raw["page_content"],
                        metadata=raw["metadata"]
                    )
                )

    def split_documents(self):
        from langchain_experimental.text_splitter import SemanticChunker
        text_splitter = SemanticChunker(self.embeddings)
        chunks = text_splitter.split_documents(self.documents)
        return chunks  

    def create_FAISS_db(self, chunks, db_name):
        from langchain_community.vectorstores import FAISS
        self.db = FAISS.from_documents(chunks, self.embeddings)
        self.db.save_local(db_name)

    def load_db(self, path):
        from langchain_community.vectorstores import FAISS
        self.db = FAISS.load_local(path, self.embeddings, allow_dangerous_deserialization = True)

    def retrieve_context(self, query, k=3):
        result = self.db.similarity_search(query, k = k)
        self.retrieved_context = "\n\n".join([doc.page_content for doc in result])
        return result

    def generate_answer(self, query):
        augmented_prompt = f"""
You are an information assistant. Your job is to answer the user's question 
ONLY using the context provided below. You must follow the rules strictly.

---------------------
CONTEXT:
{self.retrieved_context}
---------------------

USER QUESTION:
{query}

RULES:
1. Use ONLY the information in the context. If the context does not contain 
   the answer, you MUST say: "I don't know based on the provided information."

2. Never invent facts, numbers, names, or details. No hallucinations.

3. If the context partially answers the question, answer only the part 
   supported by the context and say that other information is unavailable.

4. Be concise, factual, and clear. No fluff.

5. If the question is unclear, ask the user for clarification.

6. If multiple pieces of context provide different bits of information, 
   synthesize them into a single accurate answer.

7. Do NOT mention that the information came from a retrieval system. 
   Simply answer naturally.

8. After answering, include a short SOURCES section that lists the metadata 
   (if available) of the context chunks you used.
"""
        response = self.llm.invoke(augmented_prompt)

        return response.content
    
    def ask(self, query):
        self.retrieve_context(query)
        return self.generate_answer(query)

    

