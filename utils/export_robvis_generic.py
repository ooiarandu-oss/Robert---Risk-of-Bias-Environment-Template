import pandas as pd
import io

def generate_robvis_csv(instrument, responses, study_title):
    # Mapping for generic robvis tool
    mapping = {
        "Sim": "Low",
        "Baixo risco": "Low",
        "Baixo": "Low",
        "Sem limitações graves": "Low",
        "Yes": "Low",
        "a": "Low",
        
        "Parcialmente sim": "Some concerns",
        "Parcialmente não": "Some concerns",
        "Algumas preocupações": "Some concerns",
        "Moderado": "Some concerns",
        "Incerto": "Some concerns",
        "Unclear": "Some concerns",
        "b": "Some concerns",
        "c": "Some concerns",
        
        "Não": "High",
        "Alto risco": "High",
        "Sério": "High",
        "Crítico": "High",
        "No": "High",
        "d": "High",
        
        "Nenhuma informação": "No information",
        "Sem informação": "No information",
        "Não avaliado": "No information",
        "Not applicable": "No information",
        "Não aplicável": "No information"
    }
    
    # Need to group by domains or items. robvis works best with 5-7 domains.
    # We will output one row per study.
    
    row = {"Study": study_title if study_title else "Study"}
    
    if instrument['type'] in ['robins', 'rob']:
        for dom in instrument['domains']:
            j_key = f"judgement_{dom['num']}"
            resp = responses.get(j_key, "Nenhuma informação")
            row[f"Domain {dom['num']}"] = mapping.get(resp, "No information")
    else:
        # Group by domains for NOS/JBI/DB if possible, or just list items as domains
        domains_found = {}
        for idx, item in enumerate(instrument['items']):
            dom = item.get('domain', f"Item {item['num']}")
            resp = responses.get(f"item_{idx}", "")
            if dom not in domains_found:
                domains_found[dom] = []
            domains_found[dom].append(mapping.get(resp, "No information"))
            
        i = 1
        for dom, vals in domains_found.items():
            # If any high in domain -> high, else if some concerns -> some concerns, else low
            if "High" in vals:
                row[f"Domain {i}"] = "High"
            elif "Some concerns" in vals:
                row[f"Domain {i}"] = "Some concerns"
            elif "Low" in vals:
                row[f"Domain {i}"] = "Low"
            else:
                row[f"Domain {i}"] = "No information"
            i += 1
            
    # Overall
    overall = responses.get("overall_decision", "Include")
    if overall == "Include":
        row["Overall"] = "Low"
    elif overall == "Exclude":
        row["Overall"] = "High"
    else:
        row["Overall"] = "Some concerns"
        
    row["Weight"] = 1
    
    df = pd.DataFrame([row])
    
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8')
    return csv_buffer.getvalue()
