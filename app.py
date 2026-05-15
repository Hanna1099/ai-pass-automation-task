import streamlit as st
import requests
import json
import time
from datetime import datetime

st.set_page_config(page_title="AI-Pass Automation System", layout="centered")

st.title("AI-Pass Mini Automation System")
st.subheader("Intelligent Approval Workflow")

st.write(
    "This system receives a request, processes it through an AI-assisted workflow, "
    "classifies priority/risk, generates a decision, and logs all execution steps."
)

OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")

def call_openrouter(user_input):
    url = "https://openrouter.ai/api/v1/chat/completions"

    prompt = f"""
You are an AI workflow decision engine.

Analyze the following request and return ONLY valid JSON.

Request:
{user_input}

Return JSON with this exact structure:
{{
  "decision": "APPROVE / REVIEW / REJECT",
  "priority": "LOW / MEDIUM / HIGH",
  "risk_level": "LOW / MEDIUM / HIGH",
  "confidence": "percentage number only",
  "reason": "short explanation",
  "recommended_action": "next action"
}}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": "You are an automation workflow assistant that returns structured JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    ai_text = response.json()["choices"][0]["message"]["content"]

    try:
        return json.loads(ai_text)
    except:
        return {
            "decision": "REVIEW",
            "priority": "MEDIUM",
            "risk_level": "MEDIUM",
            "confidence": "70",
            "reason": ai_text,
            "recommended_action": "Manual review required"
        }

def fallback_logic(user_input):
    text = user_input.lower()

    if "urgent" in text or "fraud" in text:
        return {
            "decision": "REVIEW",
            "priority": "HIGH",
            "risk_level": "HIGH",
            "confidence": "85",
            "reason": "Urgent or risky terms detected",
            "recommended_action": "Escalate to human review"
        }

    return {
        "decision": "APPROVE",
        "priority": "LOW",
        "risk_level": "LOW",
        "confidence": "80",
        "reason": "No major risk detected",
        "recommended_action": "Proceed normally"
    }

request_type = st.selectbox(
    "Select request type",
    [
        "Invoice Request",
        "Supplier Request",
        "Support Request",
        "General Approval Request"
    ]
)

user_input = st.text_area(
    "Enter request details",
    height=180,
    placeholder="Example: Supplier submitted an urgent invoice with missing details..."
)

use_ai = st.checkbox("Use OpenRouter AI", value=True)

if st.button("Run Workflow"):

    if not user_input.strip():
        st.warning("Please enter request details.")
    else:
        start_time = time.time()

        logs = []

        logs.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "step": "Workflow started",
            "status": "Success"
        })

        logs.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "step": "Input validated",
            "status": "Success"
        })

        try:

            if use_ai and OPENROUTER_API_KEY:
                logs.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "step": "AI processing started",
                    "status": "Success"
                })

                result = call_openrouter(user_input)

                logs.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "step": "AI response received",
                    "status": "Success"
                })

            else:
                result = fallback_logic(user_input)

                logs.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "step": "Fallback logic used",
                    "status": "Success"
                })

            execution_time = round(time.time() - start_time, 2)

            final_output = {
                "workflow_result": "Completed",
                "request_type": request_type,
                "decision": result.get("decision"),
                "priority": result.get("priority"),
                "risk_level": result.get("risk_level"),
                "confidence": result.get("confidence"),
                "explanation": result.get("reason"),
                "recommended_action": result.get("recommended_action"),
                "steps_executed": [
                    "Workflow triggered",
                    "Input validated",
                    "AI classification completed",
                    "Decision generated",
                    "Structured output returned"
                ],
                "execution_time_seconds": execution_time
            }

            logs.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "step": "Structured output generated",
                "status": "Success"
            })

            st.success("Workflow completed successfully")

            st.subheader("Structured Workflow Output")
            st.json(final_output)

            st.subheader("Execution Logs")
            st.dataframe(logs)

        except Exception as e:

            logs.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "step": "Error occurred",
                "status": str(e)
            })

            st.error("Workflow failed")

            st.dataframe(logs)
