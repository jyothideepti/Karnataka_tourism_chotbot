import streamlit as st
from rag_engine import build_knowledge_base, ask_rag
st.set_page_config(
    page_title="Karnataka Tourism AI",
    page_icon="🏛️",
    layout="wide"
)

if "kb" not in st.session_state:
    st.session_state.kb = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
st.sidebar.title("🏛️ Karnataka Tourism")
st.sidebar.caption("AI Tourism Assistant")

menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Project Information", "Technologies",
     "RAG Pipeline", "AI Chatbot"]
)

st.sidebar.divider()

uploaded_files = st.sidebar.file_uploader(
    "Upload Tourism PDF Documents",
    type=["pdf"],
    accept_multiple_files=True
)

if st.sidebar.button("Build Knowledge Base"):
    if uploaded_files:
        with st.spinner("Processing PDF documents..."):
            pdfs = [
                (file.name, file.getvalue())
                for file in uploaded_files
            ]
            st.session_state.kb = build_knowledge_base(pdfs)

        st.sidebar.success("Knowledge Base Created!")
    else:
        st.sidebar.warning("Upload PDF files first.")

# Home
if menu == "Home":

    st.title("🌿 Karnataka Tourism AI Assistant")

    st.subheader("Explore Karnataka with Artificial Intelligence")

    st.image(
        "https://images.unsplash.com/photo-1606293926075-69a00dbfde81",
        use_container_width=True
    )

    st.write("""
    Welcome to Karnataka Tourism AI Assistant.

    Explore Karnataka's:
    - Famous tourist destinations
    - Historical monuments
    - Temples
    - Waterfalls
    - Hill stations
    - Culture and festivals
    - Food and traditions
    """)

    st.success("Discover Karnataka with AI!")

# Project Information
elif menu == "Project Information":

    st.title("📌 Project Information")

    st.write("""
    Project Name: Karnataka Tourism RAG Application

    Objective:

    To develop an AI-powered chatbot that provides
    information about Karnataka tourism using PDF documents.

    Main Features:

    1. PDF document loading
    2. Text extraction
    3. Text chunking
    4. Embedding generation
    5. Vector database storage
    6. Relevant information retrieval
    7. AI answer generation
    """)

# Technologies
elif menu == "Technologies":

    st.title("🛠️ Technologies Used")

    technologies = {
        "Python": "Programming language",
        "Streamlit": "Frontend development",
        "PyPDF": "PDF text extraction",
        "OpenAI": "AI model and embeddings",
        "FAISS": "Vector database",
        "NumPy": "Numerical operations",
        "GitHub": "Code management"
    }

    for tech, description in technologies.items():
        st.subheader(tech)
        st.write(description)
        st.divider()

# RAG Pipeline
elif menu == "RAG Pipeline":

    st.title("🔄 RAG Pipeline")

    st.graphviz_chart("""
    digraph RAG {
        rankdir=TB;

        A [label="Tourism PDF Documents"];
        B [label="Load PDF"];
        C [label="Create Chunks"];
        D [label="Generate Embeddings"];
        E [label="FAISS Vector Database"];
        F [label="User Question"];
        G [label="Retrieve Relevant Chunks"];
        H [label="OpenAI LLM"];
        I [label="Final Answer"];

        A -> B -> C -> D -> E;
        E -> G;
        F -> G -> H -> I;
    }
    """)

# AI Chatbot
elif menu == "AI Chatbot":

    st.title("💬 Karnataka Tourism AI Chatbot")

    st.caption("Ask questions about Karnataka tourism.")

    if not st.session_state.kb:
        st.warning("Upload PDFs and build the Knowledge Base first.")

    else:

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input(
            "Ask about Karnataka tourism..."
        )

        if question:

            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):

                with st.spinner("AI is thinking..."):

                    try:
                        result = ask_rag(
                            question,
                            st.session_state.kb
                        )

                        answer = result["answer"]

                        st.markdown(answer)

                        if result["sources"]:
                            with st.expander("View Sources"):
                                for source in result["sources"]:
                                    st.write(source)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer
                        })

                    except Exception as e:
                        st.error(str(e))

        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

st.sidebar.divider()
st.sidebar.caption("Made with Python and OpenAI")
