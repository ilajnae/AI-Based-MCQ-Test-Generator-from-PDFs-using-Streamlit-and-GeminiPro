import streamlit as st
from components import *

# Initialize session state variables
if "mcqs" not in st.session_state:
    st.session_state.mcqs = []
if "show_test" not in st.session_state:
    st.session_state.show_test = False
if "show_report" not in st.session_state:
    st.session_state.show_report = False
if "batch_index" not in st.session_state:
    st.session_state.batch_index = 0
if "text_chunks" not in st.session_state:
    st.session_state.text_chunks = []

# App UI
st.set_page_config("PDF to MCQ Test")
st.title("📘 PDF to MCQ Test Generator")
st.write("Upload a PDF and optionally enter page numbers to generate a multiple choice test with results.")

# Upload + Page input
pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])
page_numbers_input = st.text_input("Enter page numbers (comma-separated), or leave blank for all pages", "")

# Start button
if st.button("📄 Generate Test"):
    if not pdf_file:
        st.warning("Please upload a PDF.")
    else:
        with st.spinner("Processing PDF..."):
            pages = [int(p.strip()) for p in page_numbers_input.split(",") if p.strip().isdigit()] if page_numbers_input else None

            # 1. Extract text
            raw_text = extract_text_from_pdf(pdf_file, pages)

            # 2. Split into chunks
            text_chunks = split_text_into_chunks(raw_text)
            st.session_state.text_chunks = text_chunks
            st.session_state.batch_index = 0
            st.session_state.mcqs = []

            # 3. Generate first batch of MCQs
            batch = text_chunks[0:7]
            mcqs = generate_mcqs_from_vector_store(batch)

            if not mcqs:
                st.error("Failed to generate questions. Please try a different PDF or page range.")
            else:
                st.session_state.mcqs = mcqs
                st.session_state.show_test = True
                st.session_state.show_report = False
                st.session_state.batch_index = 1  # move to next batch

# Show Test UI
if st.session_state.show_test and st.session_state.mcqs:
    run_mcq_test(st.session_state.mcqs)

    # If more chunks are left, ask to load next batch
    total_chunks = len(st.session_state.text_chunks)
    current_index = st.session_state.batch_index
    if current_index * 7 < total_chunks:
        if st.button("➕ Generate More Questions"):
            with st.spinner("Generating more questions..."):
                start = current_index * 7
                end = start + 7
                next_batch = st.session_state.text_chunks[start:end]
                new_mcqs = generate_mcqs_from_vector_store(next_batch)
                if new_mcqs:
                    st.session_state.mcqs.extend(new_mcqs)
                    st.session_state.batch_index += 1
                else:
                    st.warning("No more questions generated from the next batch.")

# Show Report UI
if st.session_state.get("show_report", False):
    show_report(st.session_state.mcqs, st.session_state.user_answers)
