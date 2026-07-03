import os
import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import io

from app.schemas.requests import ReportRequest, AiAssistantRequest
from app.services import report_generator

router = APIRouter(prefix="/api", tags=["report-and-ai"])


@router.post("/report/pdf")
def generate_pdf(req: ReportRequest):
    project_info = {
        "project_name": req.project_name,
        "client_name": req.client_name,
        "engineer_name": req.engineer_name,
        "city": req.city,
        "building_type": req.building_type,
        "revision": req.revision,
    }
    sections = [{"title": s.title, "result": s.result} for s in req.sections]
    pdf_bytes = report_generator.build_pdf(project_info, sections)

    filename = f"{req.project_name or 'HVAC_Report'}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


SYSTEM_PROMPT = """You are a senior HVAC design engineer assisting a colleague who is using \
the "Advanced HVAC AI" sizing tool (Indian SI units, ASHRAE + IS 3103 / NBC India references). \
You will be given the latest calculation results as JSON context. Answer the engineer's question \
concisely and practically: flag anything that looks oversized/undersized, mention the relevant \
standard/clause where useful, and suggest the next design check. Keep answers under 200 words \
unless the question needs a worked calculation. If context is missing or insufficient, say so \
plainly rather than guessing numbers."""


@router.post("/ai-assistant")
def ask_ai_assistant(req: AiAssistantRequest):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="AI Assistant not configured on server")

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        user_content = (
            f"Calculation context (JSON):\n{json.dumps(req.context, indent=2)}\n\n"
            f"Engineer's question: {req.question}"
        )
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
        )
        answer_text = "".join(
            block.text for block in response.content if getattr(block, "type", "") == "text"
        )
        return {"answer": answer_text}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI Assistant request failed: {exc}")
