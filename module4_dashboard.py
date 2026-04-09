# module4_dashboard.py

import streamlit as st
from module2_classifier import classify_and_route
from module3_integrations import create_trello_card

st.set_page_config(page_title="PolicyPilot", page_icon="🏦", layout="centered")

st.title("🏦 PolicyPilot")
st.subheader("AI-Powered Bank Operations Assistant")
st.markdown("Type a request below and the AI agent will classify and route it automatically.")

st.divider()

user_input = st.text_input("Enter a request:", placeholder="e.g. What is the max loan amount for personal loans?")

if st.button("Submit") and user_input:
    with st.spinner("Classifying request..."):

        # Capture the category from the classifier
        import io, sys
        captured = io.StringIO()
        sys.stdout = captured

        category = classify_and_route(user_input)

        sys.stdout = sys.__stdout__
        output = captured.getvalue()

    # Show the category as a badge
    color_map = {
        "policy_question": "🟢",
        "create_task": "🔵",
        "send_notification": "🟡",
        "trigger_workflow": "🟣",
        "unknown": "🔴"
    }
    emoji = color_map.get(category, "⚪")
    st.success(f"{emoji} Classified as: **{category}**")

    # Show routing result
    if category == "policy_question":
        st.markdown("### 📄 Policy Answer")
        # Extract the RAG answer from captured output
        for line in output.split("\n"):
            if line.startswith("  RAG Answer:"):
                answer = line.replace("  RAG Answer:", "").strip()
                st.write(answer)

    elif category == "create_task":
        st.markdown("### ✅ Trello Task Created")
        result = create_trello_card(user_input)
        st.write(f"**Task:** {result['name']}")
        st.write(f"**Trello URL:** {result['url']}")

    elif category == "send_notification":
        st.markdown("### 🔔 Notification")
        st.info("Notification routing coming soon (Module 3 extension)")

    elif category == "trigger_workflow":
        st.markdown("### ⚡ Workflow Triggered")
        st.info("Workflow trigger coming soon (Module 3 extension)")

    else:
        st.markdown("### ❓ Unknown Request")
        st.warning("Could not classify this request. It has been logged.")

    st.divider()
    st.markdown("#### 🔍 Agent Reasoning")
    st.code(output, language="text")