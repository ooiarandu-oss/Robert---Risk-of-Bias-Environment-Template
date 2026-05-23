import pandas as pd
import io

def generate_rob_excel(study_info, instrument_data, responses, overall_decision):
    # Mapping the responses to match common tool formats (robvis/critiplot)
    # Usually they expect the first column to be 'Study'
    study_name = f"{study_info.get('author', 'Unknown')} {study_info.get('year', '')}"
    if not study_name.strip():
        study_name = "Study 1"
        
    data = {'Study': [study_name]}
    for idx, r in enumerate(responses):
        item = instrument_data['items'][idx]
        col_name = item['num'] # e.g. D1, D2, S1...
        data[col_name] = [r]
        
    data['Overall'] = [overall_decision]
    data['Weight'] = [1] # Some tools require a weight column
    
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def generate_grade_excel(grade_df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        grade_df.to_excel(writer, index=False, sheet_name='GRADE')
    return output.getvalue()
