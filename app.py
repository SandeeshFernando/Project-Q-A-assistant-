"""
DOMAIN-RESTRICTED Q&A ASSISTANT
================================

YOUR TASK:
----------
Implement the functions marked with "STUDENT CODE HERE" below.
Each function has a docstring that explains exactly what it should do.
Read the docstrings carefully - they are your guide!

DEVELOPMENT STRATEGY:
---------------------
Build one tab at a time in this order:
1. Setup tab (render_setup_tab + load_knowledge_base)
2. Chat tab (render_chat_tab + build_prompt + get_ai_response)
3. Quick Questions tab (render_quick_questions_tab)

Run "streamlit run app.py" after EVERY change!

WHAT'S ALREADY PROVIDED:
------------------------
- All imports
- All constants (domains, questions, options)
- All function signatures with type hints
- initialize_session_state() (complete)
- main() (complete)
- is_setup_complete() (complete)
- render_setup_status() (complete)

WHAT YOU IMPLEMENT:
-------------------
- load_knowledge_base()
- build_prompt()
- get_ai_response()
- render_setup_tab()
- render_chat_tab()
- render_quick_questions_tab()
"""

import streamlit as st
import pandas as pd
from openai import OpenAI
from streamlit.runtime.uploaded_file_manager import UploadedFile

# ==============================================================================
# CONFIGURATION AND CONSTANTS
# ==============================================================================

# Available domains for the assistant
AVAILABLE_DOMAINS: list[str] = ["Fitness", "Travel", "Biology", "Personal Finance"]

# Prompt template questions for each domain (dict of lists)
PREBUILT_QUESTIONS: dict[str, list[str]] = {
    "Fitness": [
        "Create a beginner workout plan",
        "What should I eat before training?",
        "How do I stay consistent with fitness?",
        "How much protein do I need daily?"
    ],
    "Travel": [
        "Plan a 1-day city itinerary",
        "What are the best budget travel tips?",
        "How do I stay safe while traveling solo?",
        "What should I pack for international travel?"
    ],
    "Biology": [
        "Explain how photosynthesis works",
        "What is the difference between mitosis and meiosis?",
        "How does the immune system fight infections?",
        "What are the main functions of DNA?"
    ],
    "Personal Finance": [
        "How do I create a monthly budget?",
        "What should I know about investing?",
        "How do I build an emergency fund?",
        "Explain compound interest"
    ]
}

# Prompt style options
TONE_OPTIONS: list[str] = ["Friendly", "Professional", "Casual"]
LENGTH_OPTIONS: list[str] = ["Brief", "Moderate", "Detailed"]
AUDIENCE_OPTIONS: list[str] = ["Beginner", "Intermediate", "Advanced"]

# Required columns in the uploaded CSV
REQUIRED_CSV_COLUMNS: list[str] = ["topic", "information"]


# ==============================================================================
# HELPER FUNCTIONS (PROVIDED - DO NOT MODIFY)
# ==============================================================================

def is_setup_complete() -> bool:
    return (
        st.session_state.selected_domain is not None
        and st.session_state.knowledge_base is not None
    )


def render_setup_status() -> None:
    domain_done: bool = st.session_state.selected_domain is not None
    kb_done: bool = st.session_state.knowledge_base is not None

    if domain_done and kb_done:
        st.success(
            f"Ready — Domain: **{st.session_state.selected_domain}** | "
            f"Knowledge Base: **{st.session_state.uploaded_filename}**"
        )
    else:
        missing: list[str] = []
        if not domain_done:
            missing.append("select a domain")
        if not kb_done:
            missing.append("upload a knowledge base")
        st.warning(f"Go to the **Setup** tab to {' and '.join(missing)}.")


# ==============================================================================
# FUNCTIONS TO IMPLEMENT
# ==============================================================================

def load_knowledge_base(uploaded_file: UploadedFile) -> str:
    try:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)

        for col in REQUIRED_CSV_COLUMNS:
            if col not in df.columns:
                return f"Error: CSV is missing required column '{col}'"

        if df.empty:
            return "Error: The CSV file has no data rows."

        parts = []
        for _, row in df.iterrows():
            topic = str(row["topic"]).strip()
            info = str(row["information"]).strip()
            parts.append(f"Topic: {topic}\nInformation: {info}")

        return "\n\n".join(parts)

    except pd.errors.EmptyDataError:
        return "Error: The CSV file is empty."
    except Exception as e:
        return f"Error: {str(e)}"


def build_prompt(
    domain: str,
    knowledge_base: str,
    tone: str,
    length: str,
    audience: str,
    user_question: str
) -> str:
    return f"""You are a {domain} specialist assistant.

ROLE:
You are an expert in {domain}. Only answer questions related to {domain}.

DOMAIN CONSTRAINT:
If the question is not about {domain}, politely decline and remind the user this assistant only covers {domain}.

KNOWLEDGE BASE:
Use only the following information to answer questions:

{knowledge_base}

STYLE GUIDELINES:
- Tone: {tone}
- Response length: {length}
- Target audience: {audience}

USER QUESTION:
{user_question}

Answer based ONLY on the knowledge base above. If the answer is not in the knowledge base, say so honestly.
"""


def get_ai_response(prompt: str) -> str:
    api_key = st.session_state.get("openai_api_key")

    if not api_key:
        return "Error: Please enter your OpenAI API key in the sidebar."

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )
        content = response.choices[0].message.content
        return content if content else "Error: No response received."
    except Exception as e:
        return f"Error getting AI response: {str(e)}"


# ==============================================================================
# TAB RENDERING FUNCTIONS TO IMPLEMENT
# ==============================================================================

def render_setup_tab() -> None:
    st.header("Setup")

    selected = st.radio(
        "Select a domain:",
        AVAILABLE_DOMAINS,
        key="setup_domain"
    )
    if st.session_state.selected_domain != selected:
        st.session_state.selected_domain = selected

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload your knowledge base CSV:",
        type=["csv"],
        key="kb_uploader"
    )

    if uploaded_file is not None:
        result = load_knowledge_base(uploaded_file)

        if result.startswith("Error:"):
            st.error(result)
        else:
            st.session_state.knowledge_base = result
            st.session_state.uploaded_filename = uploaded_file.name
            st.success(f"Loaded: {uploaded_file.name}")

            with st.expander("Preview knowledge base"):
                st.text(result)


def render_chat_tab() -> None:
    render_setup_status()

    if not is_setup_complete():
        return

    domain = st.session_state.selected_domain

    user_question = st.text_input(
        "Your question:",
        placeholder=f"Ask anything about {domain}...",
        key="chat_question"
    )

    with st.expander("Response style options"):
        col1, col2, col3 = st.columns(3)
        with col1:
            tone = st.selectbox("Tone", TONE_OPTIONS, key="chat_tone")
        with col2:
            length = st.selectbox("Length", LENGTH_OPTIONS, key="chat_length")
        with col3:
            audience = st.selectbox("Audience", AUDIENCE_OPTIONS, key="chat_audience")

    if st.button("Get Answer", type="primary", key="chat_submit"):
        if not user_question.strip():
            st.warning("Please enter a question first.")
            return

        with st.spinner("Getting your answer..."):
            prompt = build_prompt(
                domain=domain,
                knowledge_base=st.session_state.knowledge_base,
                tone=tone,
                length=length,
                audience=audience,
                user_question=user_question
            )
            answer = get_ai_response(prompt)

        st.session_state.last_question = user_question
        st.session_state.last_answer = answer

    if st.session_state.last_question:
        st.markdown("---")
        st.markdown(f"**Q:** {st.session_state.last_question}")
        st.markdown(f"**A:** {st.session_state.last_answer}")


def render_quick_questions_tab() -> None:
    render_setup_status()

    if not is_setup_complete():
        return

    domain = st.session_state.selected_domain
    st.caption("Click a question below, then switch to the Chat tab to see it loaded.")

    questions = PREBUILT_QUESTIONS.get(domain, [])

    def select_question(q: str) -> None:
        st.session_state.chat_question = q

    for question in questions:
        st.button(
            question,
            key=f"preset_{domain}_{question}",
            on_click=select_question,
            args=(question,)
        )


# ==============================================================================
# STREAMLIT APP - MAIN INTERFACE (PROVIDED - DO NOT MODIFY)
# ==============================================================================

def initialize_session_state() -> None:
    defaults: dict[str, str | None] = {
        "selected_domain": None,
        "knowledge_base": None,
        "uploaded_filename": None,
        "last_question": None,
        "last_answer": None,
        "openai_api_key": None,
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def main() -> None:
    st.title("Domain Q&A Assistant")
    st.caption("A specialist assistant that only answers questions within its selected domain")

    initialize_session_state()

    with st.sidebar:
        st.header("Settings")
        st.text_input(
            "OpenAI API Key",
            type="password",
            key="openai_api_key",
            help="Enter your OpenAI API key to get real AI responses"
        )

    tab_setup, tab_chat, tab_quick = st.tabs(["Setup", "Chat", "Quick Questions"])

    with tab_setup:
        render_setup_tab()

    with tab_chat:
        render_chat_tab()

    with tab_quick:
        render_quick_questions_tab()


# ==============================================================================
# RUN THE APPLICATION
# ==============================================================================

if __name__ == "__main__":
    main()