def calculate_downs_black_score(responses, items):
    score = 0
    for idx, item in enumerate(items):
        resp = responses.get(f"item_{idx}", "")
        if item['num'] == "5":
            if resp == "Yes":
                score += 2
            elif resp == "Partial":
                score += 1
        else:
            if resp == "Yes":
                score += 1
    
    classification = "Poor"
    if score >= 26:
        classification = "Excellent"
    elif score >= 20:
        classification = "Good"
    elif score >= 15:
        classification = "Fair"
        
    return score, classification


def calculate_nos_stars(responses, items):
    stars = 0
    for idx, item in enumerate(items):
        resp = responses.get(f"item_{idx}", "")
        # This is a generic star calculation logic for NOS.
        # In a full implementation, specific answers give stars based on the manual.
        # For this prototype, we'll assign a star for option 'a', up to 9 stars.
        # Comparability domain allows 2 stars.
        
        domain = item.get('domain', '')
        if resp == "a" or resp == "Yes":
            if domain == "Comparabilidade":
                # Assuming item 5 and 6 give 1 star each, or item 5 gives 2 stars
                stars += 1
            else:
                stars += 1
                
    return min(stars, 9)
