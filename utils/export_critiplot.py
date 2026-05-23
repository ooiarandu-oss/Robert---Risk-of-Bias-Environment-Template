import pandas as pd
import io

def generate_critiplot_csv(instrument, responses, study_title):
    # This is a generic exporter for critiplot format.
    # Usually critiplot is used for JBI or NOS where items are mapped as Questions.
    
    row = {"Study": study_title if study_title else "Study"}
    
    for idx, item in enumerate(instrument['items']):
        resp = responses.get(f"item_{idx}", "")
        # Map responses to critiplot typical values
        val = ""
        if resp in ["Yes", "Sim", "a"]: val = "Yes"
        elif resp in ["No", "Não", "d"]: val = "No"
        elif resp in ["Unclear", "Incerto", "b", "c"]: val = "Unclear"
        elif resp in ["Not applicable", "Não aplicável"]: val = "Not applicable"
        
        row[f"Q{item['num']}"] = val
        
    df = pd.DataFrame([row])
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8')
    return csv_buffer.getvalue()
