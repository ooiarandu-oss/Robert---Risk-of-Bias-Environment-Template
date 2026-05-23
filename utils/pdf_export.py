import tempfile
from fpdf import FPDF

def generate_rob_pdf(study_info, instrument_data, responses, overall_decision, comments):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "Risk of Bias Assessment Report", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("helvetica", "I", 12)
    pdf.cell(0, 10, instrument_data['title'], new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 7, f"Article: {study_info.get('article_name', 'N/A')}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Reviewer: {study_info.get('reviewer', 'N/A')} | Date: {study_info.get('date', 'N/A')}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Author: {study_info.get('author', 'N/A')} | Year: {study_info.get('year', 'N/A')} | Record: {study_info.get('record_number', 'N/A')} | DOI: {study_info.get('doi', 'N/A')}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(5)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Summary Table", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "", 9)
    for idx, r in enumerate(responses):
        item = instrument_data['items'][idx]
        pdf.multi_cell(0, 7, f"[{item['domain']}] {item['num']} - {item['text']}\nAnswer: {r}")
        pdf.ln(2)
        
    pdf.ln(3)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, f"Overall Decision: {overall_decision}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 7, f"Comments: {comments}")
    
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp.name)
    return tmp.name

def generate_grade_pdf(grade_df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "GRADE Assessment Report", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    
    pdf.set_font("helvetica", "", 9)
    for index, row in grade_df.iterrows():
        text = " | ".join([f"{col}: {row[col]}" for col in grade_df.columns])
        pdf.multi_cell(0, 7, text)
        pdf.ln(2)
        
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp.name)
    return tmp.name
