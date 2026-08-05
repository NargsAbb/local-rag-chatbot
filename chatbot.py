from langchain_chroma import Chroma
from embeddings import embedding_function
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
import streamlit as st
from langchain_core.prompts import PromptTemplate
from setting import getting_file, clear_database

MODEL_NAME = "qwen2.5:7b"
MODEL_PROVIDER = "ollama"


def query_rag(query_text: str, chat_history: str):
    embed_func = embedding_function()
    db = Chroma(persist_directory="chroma", embedding_function=embed_func)

    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "---\n".join([doc.page_content for doc, _score in results])
    prompt = prompt_template.format(content=context_text, query=query_text, history=chat_history)

    try:
        response_text = llm.invoke(prompt).content
        sources = [doc.metadata.get("id", None) for doc, _score in results]
        formatted_response = f"Response: {response_text}\nSources: {sources}"
        print(formatted_response)
        return response_text, sources

    except Exception as e:
        return f" There's a problem! : {e}", []



llm = init_chat_model(MODEL_NAME,
    model_provider=MODEL_PROVIDER,
    temperature=0
)

prompt_template = PromptTemplate.from_template("""                                
You are a helpful assistant. You will be provided with a query:
{query}

and a chat history:
{history}

Your task is to retrieve relevant information from the vector store and provide a response.
Don't add any information to the answer that is not in the vector store.
Everything will be based on the retrieved information:
{content}

For every piece of information you provide, also provide the source.
If you don't know the answer, say "I don't know" (and don't provide a source).

<Answer to the question>
""")
valid_file = getting_file()
if st.button("🗑️ Clear Memory Of Files(DB)"):
        if clear_database():
            st.session_state.messages = []
            st.success("Memory Cleared Successfully")
            st.rerun()
        else:
            st.info("There Is Nothing In Memory")
if valid_file:

    # query_text = st.text_input("Hello, How Can I Help You?")
    st.title("Local RAG Chatbot")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # if query_text:
        

    if user_query := st.chat_input("Ask your question about uploaded documents..."):
        st.chat_message("user").markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        chat_history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[:-1]])

        with st.spinner("Thinking..."):
            answer, sources = query_rag(user_query, chat_history_str)

            with st.chat_message("assistant"):
                st.markdown(answer)
                if sources:
                    st.caption(f"📍 **Sources:** {', '.join(filter(None, sources))}")
                        
            st.session_state.messages.append({"role": "assistant", "content": answer})