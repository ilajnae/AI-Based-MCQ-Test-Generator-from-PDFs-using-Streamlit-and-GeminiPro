import streamlit as st
from fpdf import FPDF

def generate_report(mcqs, user_answers):
    """
    Generates a PDF report based on the user's answers.
    """
    # Create PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "MCQ Test Results", ln=True, align="C")
    
    pdf.ln(10)  # Add some space

    # Add the questions and answers
    pdf.set_font("Arial", size=12)
    for i, question_data in enumerate(mcqs):
        question = question_data["question"]
        correct_answer = question_data["answer"]
        user_answer = user_answers[i]
        explanation = question_data["explanation"]

        # Question
        pdf.multi_cell(0, 10, f"Q{i + 1}: {question}")

        # User's answer and correct answer
        pdf.cell(0, 10, f"Your answer: {user_answer}", ln=True)
        pdf.cell(0, 10, f"Correct answer: {correct_answer}", ln=True)

        # Explanation
        pdf.multi_cell(0, 10, f"Explanation: {explanation}")
        pdf.ln(5)  # Add space between questions

    # Save PDF to a file
    pdf_file = "test_report.pdf"
    pdf.output(pdf_file)

    return pdf_file


def show_report(mcqs, user_answers):
    """
    Show the test report in Streamlit and provide a download button.
    """
    # Generate the report
    report_file = generate_report(mcqs, user_answers)
    
    # Show the report in the Streamlit app
    st.title("Your Test Report")
    st.write("Download your detailed test results below.")
    
    with open(report_file, "rb") as file:
        st.download_button(
            label="Download Report",
            data=file,
            file_name=report_file,
            mime="application/pdf"
        )
