import streamlit as st
import pandas as pd
from utils.instruments_data import INSTRUMENTS
from utils.pdf_export import generate_rob_pdf
from utils.excel_export import generate_rob_excel

st.set_page_config(page_title="Risk of Bias Templates", layout="wide", page_icon="🛡️")

st.title("Risk of Bias Templates")

# Instrument Selection
instrument_keys = list(INSTRUMENTS.keys())
instrument_titles = [INSTRUMENTS[k]['title'] for k in instrument_keys]

selected_title = st.selectbox("Choose an instrument", instrument_titles)
selected_key = instrument_keys[instrument_titles.index(selected_title)]
data = INSTRUMENTS[selected_key]

st.markdown(f"### {data['title']}")
st.caption(data['sub'])

with st.expander("ℹ️ Study & Reviewer Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        reviewer = st.text_input("Reviewer Name", placeholder="Enter your name")
        article_name = st.text_input("Article Title", placeholder="Title of the study")
        author = st.text_input("Author(s)", placeholder="Authors of the study")
    with col2:
        year = st.text_input("Year of Publication", placeholder="e.g. 2024")
        record_number = st.text_input("Record Number", placeholder="Internal ID or Number")
        doi = st.text_input("DOI", placeholder="Digital Object Identifier")
        date = st.date_input("Appraisal Date")

study_info = {
    'reviewer': reviewer, 'article_name': article_name, 'author': author,
    'year': year, 'record_number': record_number, 'doi': doi, 'date': str(date)
}

st.divider()

st.markdown("### 📋 Appraisal Questionnaire")
responses = []
options = ["Yes", "No", "Unclear", "Not applicable"]

for i, item in enumerate(data['items']):
    st.markdown(f"**[{item['domain']}] {item['num']} - {item['text']}**")
    res = st.radio(f"Answer for {item['num']}", options, horizontal=True, label_visibility="collapsed", key=f"{selected_key}_{i}")
    responses.append(res)
    st.write("")

st.divider()

st.markdown("### 🎯 Overall Appraisal")
col_app1, col_app2 = st.columns(2)
with col_app1:
    overall_decision = st.radio("Overall Decision:", ["Include", "Exclude", "Seek further info"], horizontal=True)
with col_app2:
    comments = st.text_area("Comments", placeholder="Include reasons for exclusion or further info needed...")

st.divider()

col_export1, col_export2 = st.columns(2)
with col_export1:
    if st.button("📄 Generate PDF Report", use_container_width=True):
        pdf_path = generate_rob_pdf(study_info, data, responses, overall_decision, comments)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name=f"{selected_key}_report.pdf", mime="application/pdf", use_container_width=True)

with col_export2:
    if st.button("📊 Generate Excel (robvis/critiplot)", use_container_width=True):
        excel_data = generate_rob_excel(study_info, data, responses, overall_decision)
        st.download_button("📥 Download Excel", excel_data, file_name=f"{selected_key}_export.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
