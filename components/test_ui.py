import streamlit as st

def run_mcq_test(mcqs):
    """
    Displays MCQ questions one-by-one with navigation and tracks answers in session state.
    """
    if "current_q" not in st.session_state:
        st.session_state.current_q = 0
        st.session_state.user_answers = [None] * len(mcqs)
        st.session_state.test_finished = False

    current_q = st.session_state.current_q
    total_q = len(mcqs)
    question_data = mcqs[current_q]

    st.markdown(f"### Question {current_q + 1} of {total_q}")
    st.write(question_data["question"])

    selected = st.radio("Options:", question_data["options"], key=f"q_{current_q}")

    # Save the selected answer
    st.session_state.user_answers[current_q] = selected

    col1, col2 = st.columns([1, 1])
    with col1:
        if current_q < total_q - 1:
            if st.button("Next ➡️"):
                st.session_state.current_q += 1
        else:
            if st.button("✅ Finish Test"):
                st.session_state.test_finished = True

    with col2:
        if current_q > 0:
            if st.button("⬅️ Previous"):
                st.session_state.current_q -= 1

    # Show report button if finished
    if st.session_state.test_finished:
        st.success("Test Completed! 🎉")
        if st.button("📊 View Report"):
            st.session_state.show_report = True
