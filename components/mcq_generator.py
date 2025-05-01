from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import Document
from typing import List, Dict
import json
import re

def generate_mcqs_from_vector_store(chunks: List[str], num_questions: int = 5) -> List[Dict]:
    """
    Generates multiple-choice questions from a batch of text chunks using Gemini.

    Args:
        chunks (List[str]): List of text chunks (strings).
        num_questions (int): Number of MCQs to generate per batch.

    Returns:
        List[Dict]: MCQs with question, options, answer, explanation.
    """
    # Prepare the prompt
    context = "\n\n".join(chunks)
    prompt = f"""
You are a multiple choice question generator.

Based on the context below, generate {num_questions} MCQs. Each question must include:
- The question text
- Four options (A, B, C, D)
- The correct option (e.g., "B")
- A short explanation of the answer

⚠️ Return ONLY a JSON array. No Markdown formatting, no asterisks, and no extra explanation outside the JSON.

Format:
[  
  {{
    "question": "Question text?",
    "options": ["A. Option A", "B. Option B", "C. Option C", "D. Option D"],
    "answer": "B",
    "explanation": "Short explanation here."
  }},
  ...
]

Context:
{context}
"""

    model = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-pro",
        temperature=0.4,
    )

    try:
        # Get response from model
        response = model.invoke(prompt)
        raw_output = response.content.strip()
        print("Raw model output:\n", raw_output)

        # Remove Markdown code block markers (```json ... ```)
        if raw_output.startswith("```json"):
            raw_output = raw_output.replace("```json", "").replace("```", "").strip()

        # Fix invalid newlines inside JSON strings
        # This regex looks for newlines that are between quotes (i.e., in strings) and replaces them with space
        raw_output = re.sub(r'(?<!\\)\n(?=[^"]*"(?:[^"]*"[^"]*")*[^"]*$)', ' ', raw_output)

        # Try parsing the cleaned JSON string
        mcq_list = json.loads(raw_output)

        # Validate the parsed data
        def is_valid_mcq(mcq):
            return (
                isinstance(mcq, dict)
                and "question" in mcq
                and "options" in mcq and isinstance(mcq["options"], list)
                and "answer" in mcq
                and "explanation" in mcq
            )

        mcq_list = [mcq for mcq in mcq_list if is_valid_mcq(mcq)]
        if not mcq_list:
            print("❌ No valid MCQs generated.")
            return []

    except json.JSONDecodeError as je:
        print("❌ Failed to parse JSON from model output:", je)
        mcq_list = []
    except Exception as e:
        print("MCQ generation failed:", e)
        mcq_list = []

    return mcq_list
