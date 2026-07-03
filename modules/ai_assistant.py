# =========================================
# ADVANCED HVAC AI
# AI ENGINEERING ASSISTANT  (NEW - VALUE ADDITION)
# =========================================
"""
Same idea as the Claude AI assistant already wired into KBCD:
an engineer can ask a plain-language question about their latest
calculation result and get a grounded, standards-aware explanation.
Requires env var ANTHROPIC_API_KEY on the server / container.
"""
import os
import json
import streamlit as st
try:
    import anthropic
    _ANTHROPIC_AVAILABLE = True
except ImportError:
    _ANTHROPIC_AVAILABLE = False
SYSTEM_PROMPT = """You are a senior HVAC design engineer assisting a colleague who is using the "Advanced HVAC AI" sizing tool (Indian SI units, ASHRAE + IS 3103 / NBC India references). You will be given the latest calculation results as JSON context. Answer the engineer's question concisely and practically: flag anything that looks oversized/undersized, mention the relevant standard/clause where useful, and suggest the next design check. Keep answers under 200 words unless the question needs a worked calculation. If context is missing or insufficient, say so plainly rather than guessing numbers."""
def _get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key or not _ANTHROPIC_AVAILABLE:
        return None
    return anthropic.Anthropic(api_key=api_key)
def ai_assistant_tab():
    st.header("AI Engineering Assistant")
    st.markdown("---")
    client = _get_client()
    if client is None:
        st.warning(
            "AI Assistant is not configured. Set the ANTHROPIC_API_KEY environment "
            "variable on the server (see docker-compose.yml) to enable this tab."
        )
        return
    entries = st.session_state.get("report_entries", [])
    if entries:
        context_labels = [e["title"] for e in entries]
        selected = st.multiselect(
            "Include these results as context for the AI (optional)",
            context_labels,
            default=context_labels,
        )
        context = {e["title"]: e["result"] for e in entries if e["title"] in selected}
    else:
        st.info("No calculations added to the report yet — you can still ask a general question.")
        context = {}
    question = st.text_area(
        "Ask a question about your design",
        placeholder="e.g. Is my duct velocity too high for a hospital corridor? Or: does my AHU motor rating look right for this static pressure?",
        height=100,
    )
    if st.button("Ask AI Assistant") and question.strip():
        with st.spinner("Thinking..."):
            user_content = (
                f"Calculation context (JSON):\n{json.dumps(context, indent=2)}\n\n"
                f"Engineer's question: {question}"
            )
            try:
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=600,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": user_content}],
                )
                answer_text = "".join(
                    block.text for block in response.content if getattr(block, "type", "") == "text"
                )
                st.markdown("---")
                st.subheader("AI Assistant Response")
                st.markdown(answer_text)
            except Exception as exc:
                st.error(f"AI Assistant request failed: {exc}")
