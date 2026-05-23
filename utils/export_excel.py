import pandas as pd
import io

def generate_excel_report(instrument, responses, study_info):
    # Long format for Risk of Bias
    rows = []
    
    base_info = {
        "study_name": study_info.get("study_title", ""),
        "author_year": study_info.get("study_author_year", ""),
        "doi": study_info.get("study_doi", ""),
        "reviewer": study_info.get("study_reviewer", ""),
        "record_id": study_info.get("study_record", ""),
        "date": study_info.get("study_date", ""),
        "instrument": instrument['name'],
        "overall_judgement": responses.get("overall_decision", ""),
        "overall_comments": responses.get("overall_comments", "")
    }

    if instrument['type'] in ['robins', 'rob']:
        for dom in instrument['domains']:
            if 'signaling_questions' in dom:
                for sq in dom['signaling_questions']:
                    row = base_info.copy()
                    row['domain'] = dom['name']
                    row['item_id'] = sq['num']
                    row['item_text'] = sq['text']
                    row['response'] = responses.get(f"q_{dom['num']}_{sq['num']}", "")
                    row['domain_judgement'] = responses.get(f"judgement_{dom['num']}", "")
                    row['direction_of_bias'] = responses.get(f"direction_{dom['num']}", "")
                    row['justification'] = responses.get(f"justification_{dom['num']}", "")
                    rows.append(row)
            else:
                row = base_info.copy()
                row['domain'] = dom['name']
                row['item_id'] = dom['num']
                row['item_text'] = "Julgamento do domínio"
                row['response'] = ""
                row['domain_judgement'] = responses.get(f"judgement_{dom['num']}", "")
                row['direction_of_bias'] = responses.get(f"direction_{dom['num']}", "")
                row['justification'] = responses.get(f"justification_{dom['num']}", "")
                rows.append(row)
    else:
        for idx, item in enumerate(instrument['items']):
            row = base_info.copy()
            row['domain'] = item.get('domain', '')
            row['item_id'] = item['num']
            row['item_text'] = item['text']
            row['response'] = responses.get(f"item_{idx}", "")
            row['justification'] = responses.get(f"just_{idx}", "")
            # calculate score for specific items if D&B
            if instrument['type'] == 'db':
                row['score'] = "" # We could add individual score logic here
            rows.append(row)

    df = pd.DataFrame(rows)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return buffer.getvalue()


def generate_grade_excel(grade_df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        grade_df.to_excel(writer, index=False)
    return buffer.getvalue()
