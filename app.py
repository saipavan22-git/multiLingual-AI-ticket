import streamlit as st
from evaluator import generate_response, evaluate_response

# Page title
st.title("Multilingual AI Support Ticket Evaluator")

# Description
st.write("Evaluate AI-generated customer support responses.")

# Language selector
language = st.selectbox(
    "Select Language",
    ["English", "Hindi", "Telugu"]
)

# User input
ticket = st.text_area("Enter Customer Support Ticket")

# Button
if st.button("Evaluate AI Response"):

    response = generate_response(ticket, language)

    evaluation = evaluate_response(ticket, response)

    st.subheader("AI Response")
    st.success(response)

    st.subheader("Evaluation Results")

    st.progress(evaluation["score"] / 100)

    st.metric(
        "Overall Score",
        f'{evaluation["score"]}/100'
    )

    st.metric(
        "Escalation Needed",
        evaluation["escalation"]
    )

    st.metric(
        "Hallucination Risk",
        evaluation["hallucination"]
    )