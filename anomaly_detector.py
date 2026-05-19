import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(metrics):

    df = pd.DataFrame(metrics)

    features = df[['cpu', 'memory', 'disk_io', 'restarts']]

    model = IsolationForest(
        contamination=0.3,
        random_state=42
    )

    df['anomaly'] = model.fit_predict(features)

    anomalies = []

    for _, row in df.iterrows():

        if row['anomaly'] == -1:

            anomalies.append({
                "pod": row['pod'],
                "cpu": row['cpu'],
                "memory": row['memory'],
                "disk_io": row['disk_io'],
                "restarts": row['restarts']
            })

    return anomalies