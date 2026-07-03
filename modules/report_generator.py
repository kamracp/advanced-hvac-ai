import io
from datetime import date

import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def _init_session_report():
    if "report_entries" not in st.session_state:
        st.session_state["report_entries"] = []


def add_to_report(section_title, result):
    _init_session_report()
    st.session_state["report_entries"] = [
        e for e in st.session_state["report_entries"] if e["title"] != section_title
    ]
    st.session_state["report_entries"].append({"title": section_title, "result": result})


def _build_pdf(project_info, entries):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=15 * mm, bottomMargin=15 * mm, leftMargin=15 * mm, rightMargin=15 * mm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontSize=18, spaceAfter=4)
    h2_style = ParagraphStyle("H2Style", parent=styles["Heading2"], spaceBefore=10, spaceAfter=6)
    normal = styles["Normal"]

    story = []
    story.append(Paragraph("Kamra Engineering Solutions", title_style))
    story.append(Paragraph("Advanced HVAC AI - Engineering Calculation Report", styles["Heading3"]))
    story.append(Spacer(1, 8))

    header_data = [
        ["Project Name", project_info.get("project_name", ""), "Report Date", str(date.today())],
        ["Client", project_info.get("client_name", ""), "Building Type", project_info.get("building_type", "")],
        ["Engineer", project_info.get("engineer_name", ""), "Revision", project_info.get("revision", "R0")],
        ["City", project_info.get("city", ""), "Design Basis", "ASHRAE / IS"],
    ]
    header_table = Table(header_data, colWidths=[35 * mm, 55 * mm, 35 * mm, 55 * mm])
    header_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 14))

    if not entries:
        story.append(Paragraph("No calculations were added to this report. Use the Add to Report button on any calculation tab, then re-export.", normal))
    else:
        for entry in entries:
            story.append(Paragraph(entry["title"], h2_style))
            rows = [["Parameter", "Value"]] + [[k, str(v)] for k, v in entry["result"].items()]
            t = Table(rows, colWidths=[95 * mm, 75 * mm])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f5f8")]),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(t)
            story.append(Spacer(1, 10))

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "Disclaimer: Preliminary sizing output for design-support purposes only. Final selection to be verified by a qualified engineer against project-specific conditions, manufacturer software, and applicable statutory codes.",
        ParagraphStyle("Disclaimer", parent=normal, fontSize=7, textColor=colors.grey),
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()


def report_tab():
    st.header("PDF Report Export")
    st.markdown("---")
    _init_session_report()

    st.subheader("Project & Company Details")
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name", value="", key="rep_project")
        client_name = st.text_input("Client Name", value="", key="rep_client")
        engineer_name = st.text_input("Engineer Name", value="", key="rep_engineer")
    with col2:
        city = st.text_input("City", value="", key="rep_city")
        building_type = st.text_input("Building Type", value="", key="rep_building")
        revision = st.text_input("Revision", value="R0", key="rep_revision")

    st.markdown("---")
    st.subheader("Sections in this Report")
    entries = st.session_state["report_entries"]
    if entries:
        for e in entries:
            st.write("- " + e["title"])
    else:
        st.info("No sections added yet. Go to any calculation tab, run a calculation, then click Add to Report below its results.")

    if st.button("Generate PDF Report"):
        project_info = {
            "project_name": project_name,
            "client_name": client_name,
            "engineer_name": engineer_name,
            "city": city,
            "building_type": building_type,
            "revision": revision,
        }
        pdf_bytes = _build_pdf(project_info, entries)
        st.success("PDF Report Generated")
        st.download_button("Download PDF Report", data=pdf_bytes, file_name=(project_name or "HVAC_Report") + "_" + str(date.today()) + ".pdf", mime="application/pdf")
