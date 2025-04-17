import os
import openai
import streamlit as st
from dotenv import load_dotenv

# Load your OpenAI API key from environment or set it directly
load_dotenv()
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_sequence(persona, pain_point, steps, product_value=None, tone=None):
    system_prompt = (
        "You are an expert B2B SaaS marketer and cold email writer. "
        "You write engaging cold email sequences (3–6 steps), each with a subject line and body. "
        "Emails should sound natural, show empathy, and avoid sounding like spam. "
        "You vary tone/pitch slightly across steps (e.g. insight, question, humor, social proof)."
    )

    user_prompt = f"""
    Target persona: {persona}
    Key pain point: {pain_point}
    Product value prop: {product_value if product_value else 'Skip'}
    Preferred tone: {tone if tone else 'Friendly and helpful'}
    Number of Steps: {steps}

    Generate a {steps}-step cold email sequence. Each step should include:
    - Subject line
    - Email body (2–4 sentences max)
    - Vary tone/pitch across steps (e.g., consultative, casual, bold, social proof)
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,
    )

    return response['choices'][0]['message']['content']

# Streamlit App
st.set_page_config(page_title="Cold Email Sequence Generator", layout="centered")
st.title("🧊 Cold Email Sequence Generator")

persona = st.text_input("Target Persona", "Head of Growth at a B2B SaaS startup")
pain_point = st.text_input("Key Pain Point", "Low reply rates despite personalization")
product_value = st.text_input("Product Value Prop (optional)", "Embed social proof from top customers in outbound")
tone = st.text_input("Preferred Tone (optional)", "Friendly but sharp")

if st.button("Generate Sequence"):
    with st.spinner("Generating your sequence..."):
        sequence = generate_sequence(persona, pain_point, product_value, tone)
        st.markdown("---")
        st.markdown(sequence)
        st.markdown("---")