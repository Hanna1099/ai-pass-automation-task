# AI-Pass Mini Automation System

## Overview

This project implements a simplified AI-assisted Intelligent Approval Workflow inspired by AI-Pass workflow automation systems.

The application receives a request input, processes it through an automation workflow, uses AI for classification and decision support, generates structured outputs, and logs execution steps in real time.

The system is deployed live using Streamlit Cloud and integrated with OpenRouter API for AI processing.

---

## Features

- AI-assisted workflow processing
- Intelligent approval decision generation
- Priority and risk classification
- Structured JSON output
- Execution logging and monitoring
- Live deployment with public access
- OpenRouter AI integration
- Fallback workflow logic

---

## Workflow Architecture

Trigger Layer
→ User submits request through Streamlit interface

Processing Layer
→ Input validation and workflow orchestration

AI Layer
→ OpenRouter API processes request and generates classification

Decision Layer
→ AI generates:
- decision
- priority
- risk level
- explanation
- recommended action

Output Layer
→ Structured JSON response returned to user

Logging Layer
→ Execution logs generated for all workflow steps

---

## AI Integration Used

- OpenRouter API
- LLM-based classification and decision support
- AI-generated explanations and workflow recommendations

---

## Trigger Flow

The workflow starts using a manual trigger through the Streamlit web interface.

Workflow Steps:
1. Workflow triggered
2. Input validated
3. AI classification completed
4. Decision generated
5. Structured output returned
6. Execution logs generated

---

## Structured Output Example

```json
{
  "decision": "REVIEW",
  "priority": "HIGH",
  "risk_level": "MEDIUM",
  "confidence": 78,

---

## Deployment

Live App:
[AI-Pass Live Application](https://ai-pass-automation-task-jvya7xssxup7lbqgjhurbh.streamlit.app/)

GitHub Repository:
[GitHub Repository](https://github.com/Hanna1099/ai-pass-automation-task)
  "recommended_action": "Request missing information before approval"
}
