from typing import Optional

## here we define some utility functions to query the database
# Mock patients database
fake_patients_db = {
    # Example patient records
    "patient1": {
        "cni": "123456789",
        "crashId": "crash123",
        "severity": "critical",
        "recordId": "record123",
        "admissionReason": "Road Crash",
        "admissionTime": "2023-10-01T12:00:00Z",
        "diagnosis": "Severe injuries",
        "treatment": "Emergency surgery",
        "finalStatus": "deceased"
    },
    "patient2": {
        "cni": "987654321",
        "crashId": "crash456",
        "severity": "moderate",
        "recordId": "record456",
        "admissionReason": "Road Crash",
        "admissionTime": "2023-10-02T14:30:00Z",
        "diagnosis": "Fractures",
        "treatment": "Casting and observation",
        "finalStatus": "stable"
    },
    "patient3": {
        "cni": "456789123",
        "crashId": "crash789",
        "severity": "minor",
        "recordId": "record789",
        "admissionReason": "Road Crash",
        "admissionTime": "2023-10-03T09:15:00Z",
        "diagnosis": "Minor injuries",
        "treatment": "Rest and medication",
        "finalStatus": "recovered"
    },
    "patient4": {
        "cni": "321654987",
        "crashId": "crash101",
        "severity": "critical",
        "recordId": "record101",
        "admissionReason": "Road Crash",
        "admissionTime": "2023-10-04T11:45:00Z",
        "diagnosis": "Life-threatening injuries",
        "treatment": "ICU care",
        "finalStatus": "deceased"
    },
    "patient5": {
        "cni": "654321789",
        "crashId": "crash202",
        "severity": "moderate",
        "recordId": "record202",
        "admissionReason": "Road Crash",
        "admissionTime": "2023-10-05T08:30:00Z",
        "diagnosis": "Concussion",
        "treatment": "Observation and rest",
        "finalStatus": "stable"
    },
    "patient6": {
        "cni": "789123456",
        "crashId": "crash303",
        "severity": "minor",
        "recordId": "record303",
        "admissionReason": "Road Crash",
        "admissionTime": "2023-10-06T10:00:00Z",
        "diagnosis": "Bruises and cuts",
        "treatment": "First aid and observation",
        "finalStatus": "recovered"
    }
}
def record_with_cni_admission_time(cni: str, interval_probable_admission_debut: str, interval_probable_admission_fin: str, crashId:  Optional[str]):
    """
    Retrieve a patient's record based on their CNI probable admission dates and optional crash ID.
    """
    # Filter records based on CNI and admission time interval
    records = []
    for patient_id, record in fake_patients_db.items():
        if record["cni"] == cni:
            if crashId and record["crashId"] != crashId:
                continue
            if interval_probable_admission_debut <= record["admissionTime"] <= interval_probable_admission_fin:
                records.append(record)
    
    return records

def record_with_cni_crashId(cni: str, crashId: str):
    """
    Retrieve a patient's record based on their CNI and crash ID.
    """
    records = []
    for patient_id, record in fake_patients_db.items():
        if record["cni"] == cni and record["crashId"] == crashId:
            records.append(record)
    return records

def record_with_crashId(crashId: str):
    """
    Retrieve a patient's record based on their crash ID.
    """
    records = []
    for patient_id, record in fake_patients_db.items():
        if record["crashId"] == crashId:
            records.append(record)
    return records

def record_within_admision_time(
    interval_probable_admission_debut: str, 
    interval_probable_admission_fin: str
):
    """
    Retrieve all patient records within the specified admission time interval.
    """
    records = []
    for patient_id, record in fake_patients_db.items():
        if interval_probable_admission_debut <= record["admissionTime"] <= interval_probable_admission_fin:
            records.append(record)
    
    return records