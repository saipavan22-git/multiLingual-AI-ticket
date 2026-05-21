from groq import Groq
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import os

# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Translate text
def translate_text(text, target_lang):

    if not text:
        return text

    translated = GoogleTranslator(
        source="auto",
        target=target_lang
    ).translate(text)

    return translated


# Generate AI response
def generate_response(ticket, target_language):

    language_map = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te"
    }

    original_language = language_map[target_language]

    english_ticket = translate_text(ticket, "en")

    prompt = f"""
    You are a professional customer support assistant.

    Customer Ticket:
    {english_ticket}

    Generate a professional and helpful customer support response.
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response = completion.choices[0].message.content

    if original_language != "en":
        response = translate_text(response, original_language)

    return response


# Evaluate AI response
def evaluate_response(ticket, response):

    score = 100

    escalation = "No"
    hallucination = "Low"

    english_ticket = translate_text(ticket, "en")

    if "refund" in english_ticket.lower():
        escalation = "Yes"

    if "charged twice" in english_ticket.lower():
        escalation = "Yes"

    if "cancel" in english_ticket.lower():
        escalation = "Yes"

    if len(response) < 40:
        score -= 20

    if "guaranteed" in response.lower():
        hallucination = "Medium"
        score -= 20

    if "sorry" in response.lower():
        score += 5

    return {
        "score": score,
        "escalation": escalation,
        "hallucination": hallucination
    }