from flask import Flask, jsonify
import json

from anomaly_detector import detect_anomalies
from correlation_engine import correlate
from nlp_generator import generate_nlp_report

app = Flask(__name__)

@app.route('/analyze')

def analyze():

    with open('metrics.json') as f:
        metrics = json.load(f)

    anomalies = detect_anomalies(metrics)

    final_reports = []

    for anomaly in anomalies:

        correlated = correlate(anomaly)

        report = generate_nlp_report(correlated)

        final_reports.append({
            "pod": correlated['pod'],
            "issue": correlated['issue'],
            "report": report
        })

    return jsonify(final_reports)

if __name__ == '__main__':
    app.run(debug=True)