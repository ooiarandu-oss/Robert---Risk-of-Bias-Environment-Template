import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from .scoring import calculate_downs_black_score, calculate_nos_stars

def generate_pdf_report(instrument, responses, study_info):
    if instrument['type'] == 'db':
        return generate_downs_black_pdf(instrument, responses, study_info)
    elif instrument['type'] == 'jbi':
        return generate_jbi_pdf(instrument, responses, study_info)
    else:
        return generate_generic_rob_pdf(instrument, responses, study_info)

def generate_downs_black_pdf(instrument, responses, study_info):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], textColor=colors.HexColor('#085041'), alignment=1)
    elements.append(Paragraph("Downs & Black Checklist Report", title_style))
    elements.append(Spacer(1, 20))

    # Metadata
    meta_data = [
        ["Article:", study_info.get('study_title', '')],
        ["Authors:", study_info.get('study_author_year', '')],
        ["Evaluator:", study_info.get('study_reviewer', '')],
        ["DOI:", study_info.get('study_doi', '')],
        ["Record Number:", study_info.get('study_record', '')],
        ["Date:", study_info.get('study_date', '')]
    ]
    t_meta = Table(meta_data, colWidths=[100, 400])
    t_meta.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#4B5563')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_meta)
    elements.append(Spacer(1, 20))

    # Score Box
    score, classification = calculate_downs_black_score(responses, instrument['items'])
    score_data = [
        ["Total Score:", f"{score} / 28"],
        ["Overall Methodological Quality:", classification]
    ]
    t_score = Table(score_data, colWidths=[200, 100])
    t_score.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#E1F5EE')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#085041')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1D9E75')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(t_score)
    elements.append(Spacer(1, 20))

    # Domains
    domains = {}
    for idx, item in enumerate(instrument['items']):
        dom = item['domain']
        if dom not in domains:
            domains[dom] = []
        resp = responses.get(f"item_{idx}", "")
        just = responses.get(f"just_{idx}", "")
        
        # Max score calculation
        max_score = 2 if item['num'] == "5" else 1
        item_score = 0
        if item['num'] == "5":
            if resp == "Yes": item_score = 2
            elif resp == "Partial": item_score = 1
        else:
            if resp == "Yes": item_score = 1
            
        domains[dom].append([item['num'], Paragraph(item['text'], styles['Normal']), max_score, item_score, Paragraph(just, styles['Normal'])])

    for dom, rows in domains.items():
        elements.append(Paragraph(dom, styles['Heading2']))
        table_data = [["Item", "Question", "Max", "Score", "Notes"]] + rows
        t_dom = Table(table_data, colWidths=[40, 250, 30, 40, 170])
        t_dom.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        elements.append(t_dom)
        elements.append(Spacer(1, 15))

    # Reference
    elements.append(Spacer(1, 20))
    ref = "Reference: Downs SH, Black N. The feasibility of creating a checklist for the assessment of the methodological quality both of randomised and non-randomised studies of health care interventions. J Epidemiol Community Health. 1998;52(6):377-84."
    elements.append(Paragraph(ref, styles['Italic']))

    doc.build(elements)
    return buffer.getvalue()


def generate_jbi_pdf(instrument, responses, study_info):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], alignment=1)
    elements.append(Paragraph("JBI Critical Appraisal Report", title_style))
    elements.append(Paragraph(f"Checklist for {instrument['report_title']}", styles['Heading3']))
    elements.append(Spacer(1, 15))

    # Metadata
    meta_data = [
        ["Article:", study_info.get('study_title', '')],
        ["Reviewer:", study_info.get('study_reviewer', '')],
        ["Date:", study_info.get('study_date', '')],
        ["Author, Year:", study_info.get('study_author_year', '')],
        ["Record Number:", study_info.get('study_record', '')],
        ["DOI:", study_info.get('study_doi', '')]
    ]
    t_meta = Table(meta_data, colWidths=[100, 400])
    t_meta.setStyle(TableStyle([('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
    elements.append(t_meta)
    elements.append(Spacer(1, 20))

    # Summary Table
    elements.append(Paragraph("Summary Table", styles['Heading2']))
    table_data = [["Item", "Question", "Answer", "Comments"]]
    for idx, item in enumerate(instrument['items']):
        resp = responses.get(f"item_{idx}", "")
        just = responses.get(f"just_{idx}", "")
        table_data.append([item['num'], Paragraph(item['text'], styles['Normal']), resp, Paragraph(just, styles['Normal'])])

    t_dom = Table(table_data, colWidths=[30, 270, 70, 160])
    t_dom.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(t_dom)
    elements.append(Spacer(1, 20))

    # Overall Decision
    elements.append(Paragraph("Overall Decision:", styles['Heading3']))
    decision = responses.get("overall_decision", "")
    elements.append(Paragraph(decision, styles['Normal']))
    elements.append(Spacer(1, 10))
    
    elements.append(Paragraph("Comments:", styles['Heading3']))
    comments = responses.get("overall_comments", "")
    elements.append(Paragraph(comments if comments else "None", styles['Normal']))
    
    # Reference
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("References: Peters, M. D. J., et al. (2015). JBI reviewers' manual. JBI, 2020. All rights reserved.", styles['Italic']))

    doc.build(elements)
    return buffer.getvalue()


def generate_generic_rob_pdf(instrument, responses, study_info):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"{instrument['name']} Report", styles['Heading1']))
    elements.append(Spacer(1, 15))
    
    for k, v in study_info.items():
        elements.append(Paragraph(f"<b>{k}:</b> {v}", styles['Normal']))
        
    elements.append(Spacer(1, 20))

    if instrument['type'] in ['robins', 'rob']:
        for dom in instrument['domains']:
            elements.append(Paragraph(f"Domain {dom['num']}: {dom['name']}", styles['Heading3']))
            if 'signaling_questions' in dom:
                for sq in dom['signaling_questions']:
                    key = f"q_{dom['num']}_{sq['num']}"
                    resp = responses.get(key, "")
                    elements.append(Paragraph(f"<b>{sq['num']}</b> {sq['text']} - <i>{resp}</i>", styles['Normal']))
            
            j_key = f"judgement_{dom['num']}"
            resp = responses.get(j_key, "")
            elements.append(Paragraph(f"<b>Judgement:</b> {resp}", styles['Normal']))
            just_key = f"justification_{dom['num']}"
            just = responses.get(just_key, "")
            elements.append(Paragraph(f"<b>Justification:</b> {just}", styles['Normal']))
            elements.append(Spacer(1, 10))
    else:
        table_data = [["Item", "Question", "Answer", "Notes"]]
        for idx, item in enumerate(instrument['items']):
            resp = responses.get(f"item_{idx}", "")
            just = responses.get(f"just_{idx}", "")
            table_data.append([item['num'], Paragraph(item['text'], styles['Normal']), resp, Paragraph(just, styles['Normal'])])
        
        t_dom = Table(table_data, colWidths=[30, 270, 70, 160])
        t_dom.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        elements.append(t_dom)

    doc.build(elements)
    return buffer.getvalue()


def generate_grade_pdf(grade_df):
    buffer = io.BytesIO()
    # GRADE tables are wide, use landscape
    from reportlab.lib.pagesizes import A4, landscape
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("GRADE Assessment Table", styles['Heading1']))
    elements.append(Spacer(1, 15))

    # Convert DataFrame to list of lists for Table
    columns = list(grade_df.columns)
    data = [[Paragraph(c, styles['Normal']) for c in columns]]
    
    for _, row in grade_df.iterrows():
        data.append([Paragraph(str(val), styles['Normal']) for val in row])
        
    col_w = (landscape(A4)[0] - 40) / len(columns)
    t = Table(data, colWidths=[col_w] * len(columns))
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1D9E75')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    
    elements.append(t)
    doc.build(elements)
    return buffer.getvalue()
