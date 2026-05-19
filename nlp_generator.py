def generate_nlp_report(result):

    pod = result['pod']
    issue = result['issue']
    impacted = result['impacted_services']

    report = f"""
AI Infrastructure Insight

Pod: {pod}

Detected Issue:
{issue}

Potential Impact:
"""

    if impacted:
        for service in impacted:
            report += f"\n- {service} may experience degraded performance"

    else:
        report += "\n- No downstream impact detected"

    report += """

Recommended Actions:
- Inspect pod logs
- Verify resource limits
- Scale deployment if required
"""

    return report