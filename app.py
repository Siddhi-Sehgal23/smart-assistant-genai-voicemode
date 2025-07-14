import streamlit as st
from utils.pdf_parser import parse_file
from backend.summarizer import summarize_text
from backend.qa_engine import answer_question, generate_logic_questions
from backend.evaluator import evaluate_answer
from utils.vector_store import create_vector_store, retrieve_relevant_chunks

st.set_page_config(page_title="Smart Assistant with Voice", layout="wide")
st.title("🧠 Smart Research Assistant (with Voice & Evaluation Mode)")

uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
if not uploaded_file:
    st.warning("📤 Please upload a document to continue.")
    st.stop()

with st.spinner("📖 Reading your file..."):
    full_text = parse_file(uploaded_file)

if not full_text.strip():
    st.error("❌ No text could be extracted from the file.")
    st.stop()

st.subheader("📌 Summary")
summary = summarize_text(full_text)
st.success(summary)

vector_index = create_vector_store(full_text)

mode = st.radio("Choose Mode", ["Ask Anything", "Challenge Me", "Evaluation Mode"])

if mode == "Ask Anything":
    user_q = st.text_input("❓ Ask a question from the document")
    if user_q:
        chunks = retrieve_relevant_chunks(user_q, vector_index)
        response, justification = answer_question(user_q, chunks)
        st.write("**Answer:**", response)
        st.info(f"Justification: {justification}")

elif mode == "Challenge Me":
    questions = generate_logic_questions(full_text)
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        user_ans = st.text_input("Your Answer:", key=f"q{i}")
        if user_ans:
            result = evaluate_answer(q['question'], user_ans, q['answer'])
            st.write(result)

elif mode == "Evaluation Mode":
    st.warning("🚧 Evaluation Mode is a placeholder for future enhancement.")
    st.info("You can implement scoring, report cards, and adaptive feedback here!")

st.markdown("---")
st.subheader("🎙️ Voice Input (Experimental)")
st.info("🎤 Voice input is a placeholder. You can integrate it using speech_recognition and pyttsx3 libraries.")