from dependency_mapper import get_impacted_services

def correlate(anomaly):

    cpu = anomaly['cpu']
    memory = anomaly['memory']
    disk = anomaly['disk_io']
    restarts = anomaly['restarts']

    issue = "Unknown"

    if cpu > 80 and memory > 80:
        issue = "Possible Memory Leak"

    elif disk > 80:
        issue = "PVC / Database I/O Overload"

    elif restarts >= 3:
        issue = "Crash Loop Detected"

    impacted = get_impacted_services(anomaly['pod'])

    return {
        "pod": anomaly['pod'],
        "issue": issue,
        "impacted_services": impacted
    }