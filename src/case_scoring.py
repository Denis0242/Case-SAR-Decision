def case_priority(score, red_flags):
    if score >= 80 or red_flags >= 6:
        return 'Critical'
    if score >= 65 or red_flags >= 4:
        return 'High'
    if score >= 50:
        return 'Moderate'
    return 'Low'
