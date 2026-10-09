from langchain_groq import ChatGroq
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from core.config import Config

class RAGChainBuilder:
    def __init__(self, vector_store):
        # 1. The Vector Store (The Database connection passed in from data_ingestion.py)
        self.vector_store = vector_store
        
        # 2. The Generation Model (The Groq LLM)
        self.model = ChatGroq(model=Config.RAG_MODEL, temperature=0.5)

    def _get_history(self, session_id: str) -> BaseChatMessageHistory:
        """Connects to Redis to retrieve chat history."""
        return RedisChatMessageHistory(
            session_id=session_id,
            url=Config.REDIS_URL
        )
    
    def build_chain(self):
        """Assembles the LangChain RAG architecture."""
        
        # STEP 1: CONFIGURE THE RETRIEVER
        # Tells the database to always return the top 15 closest matching reviews
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 15})

        # STEP 2: CONTEXTUALIZE THE QUESTION (HISTORY-AWARE)
        # If the user asks a follow-up question like "Does it have a good battery?", 
        # this prompt forces the AI to look at the chat history and rewrite it to 
        # "Does the Samsung Galaxy S23 have a good battery?" before searching AstraDB.
        context_prompt = ChatPromptTemplate.from_messages([
            ("system", "Given the chat history and the user's latest question, rewrite the question into a standalone question that can be understood without the chat history."),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])
        
        history_aware_retriever = create_history_aware_retriever(
            self.model, retriever, context_prompt
        )

        # STEP 3: ANSWER THE QUESTION USING DATABASE CONTEXT
        # This is the final prompt sent to Groq. We inject the retrieved reviews 
        # as {context} and ask the AI to answer the user's {input}.
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful e-commerce bot answering product-related queries using reviews and titles.
                          Stick strictly to the provided context. Be concise and helpful.
                          
                          CONTEXT:
                          {context}"""),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])

        question_answer_chain = create_stuff_documents_chain(
            self.model, qa_prompt
        )

        # STEP 4: ASSEMBLE THE FINAL RAG CHAIN
        # We glue the retriever (Step 2) and the answer chain (Step 3) together.
        rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        # STEP 5: ATTACH MEMORY
        # Wrap the whole chain in a memory class so it automatically remembers past messages.
        return RunnableWithMessageHistory(
            rag_chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
