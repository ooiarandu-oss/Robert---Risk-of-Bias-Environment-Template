import streamlit as st
import pandas as pd
from utils.pdf_export import generate_grade_pdf
from utils.excel_export import generate_grade_excel

st.set_page_config(page_title="GRADE Assessment", layout="wide", page_icon="📊")

st.title("GRADE Assessment Table")

# Initialize session state for the dataframe
if 'grade_df' not in st.session_state:
    st.session_state.grade_df = pd.DataFrame({
        'Outcome': ['Outcome 1'],
        'Author, Year - Study 1': [''],
        'Risk of Bias': ['Not serious'],
        'GRADE': ['Moderate']
    })

if 'study_count' not in st.session_state:
    st.session_state.study_count = 1

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("➕ Add Study Column"):
        st.session_state.study_count += 1
        col_name = f'Author, Year - Study {st.session_state.study_count}'
        
        # We need to insert it before 'Risk of Bias' and 'GRADE'
        cols = list(st.session_state.grade_df.columns)
        rob_idx = cols.index('Risk of Bias')
        
        st.session_state.grade_df.insert(rob_idx, col_name, '')
        st.rerun()

with col2:
    if st.button("➕ Add Outcome Row"):
        new_row = {col: '' for col in st.session_state.grade_df.columns}
        new_row['Outcome'] = f'Outcome {len(st.session_state.grade_df) + 1}'
        new_row['Risk of Bias'] = 'Not serious'
        new_row['GRADE'] = 'Moderate'
        st.session_state.grade_df = pd.concat([st.session_state.grade_df, pd.DataFrame([new_row])], ignore_index=True)
        st.rerun()

# Config columns for data editor
column_config = {
    'Outcome': st.column_config.TextColumn("Outcome", required=True),
    'Risk of Bias': st.column_config.SelectboxColumn(
        "Risk of Bias",
        options=["Not serious", "Serious", "Very serious"],
        required=True
    ),
    'GRADE': st.column_config.SelectboxColumn(
        "GRADE",
        options=["High", "Moderate", "Low", "Very low"],
        required=True
    )
}

st.session_state.grade_df = st.data_editor(
    st.session_state.grade_df,
    column_config=column_config,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)

st.divider()

st.markdown("### Export GRADE Table")
col_e1, col_e2 = st.columns(2)

with col_e1:
    if st.button("📄 Generate PDF", use_container_width=True):
        pdf_path = generate_grade_pdf(st.session_state.grade_df)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name="GRADE_assessment.pdf", mime="application/pdf", use_container_width=True)

with col_e2:
    if st.button("📊 Generate Excel", use_container_width=True):
        excel_data = generate_grade_excel(st.session_state.grade_df)
        st.download_button("📥 Download Excel", excel_data, file_name="GRADE_assessment.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
