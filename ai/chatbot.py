import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")


def get_financial_advice(user_query, income, expenses, savings, goal, months):
    prompt = f"""
    You are a friendly financial mentor for college students.

    Student Data:
    Monthly Income: ₹{income}
    Monthly Expenses: ₹{expenses}
    Monthly Savings: ₹{savings}
    Goal Amount: ₹{goal}
    Duration: {months} months

    User Question:
    {user_query}

    Provide:
    1. Clear financial advice
    2. Spending improvement suggestions
    3. Simple explanation of risks if relevant
    4. Motivation to build saving discipline

    Keep response short, practical and student-friendly.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"
