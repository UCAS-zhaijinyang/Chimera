import pandas as pd

def validate_ehr_data(file_path):
    # Load the EHR data
    ehr_data = pd.read_csv(file_path)

    # Check for missing data
    missing_data = ehr_data.isnull().sum()
    print(f"Missing data:\n{missing_data}\n")

    # Check for duplicate entries
    duplicate_entries = ehr_data.duplicated().sum()
    print(f"Duplicate entries: {duplicate_entries}\n")

    # Check for inconsistencies in date formats
    if 'date_of_birth' in ehr_data.columns:
        invalid_dates = ehr_data[~pd.to_datetime(ehr_data['date_of_birth'], errors='coerce').notnull()]['date_of_birth']
        print(f"Invalid date formats in 'date_of_birth':\n{invalid_dates}\n")

    # Check for inconsistencies in medical codes (example: ICD-10)
    if 'diagnosis_code' in ehr_data.columns:
        invalid_codes = ehr_data[~ehr_data['diagnosis_code'].str.match(r'^[A-Za-z0-9]{3,7}$')]['diagnosis_code']
        print(f"Invalid diagnosis codes (ICD-10 format):\n{invalid_codes}\n")

    # Check for inconsistencies in numeric fields (example: blood pressure)
    if 'blood_pressure' in ehr_data.columns:
        invalid_blood_pressure = ehr_data[~ehr_data['blood_pressure'].str.contains(r'^\d+\/\d+$')]['blood_pressure']
        print(f"Invalid blood pressure formats:\n{invalid_blood_pressure}\n")

    # Save the results to a file
    results = {
        'missing_data': missing_data.to_dict(),
        'duplicate_entries': duplicate_entries,
        'invalid_dates': invalid_dates.tolist(),
        'invalid_codes': invalid_codes.tolist(),
        'invalid_blood_pressure': invalid_blood_pressure.tolist()
    }
    return results

# Example usage:
if __name__ == "__main__":
    file_path = '/home/zjy/Chimera/ehr_data.csv'
    results = validate_ehr_data(file_path)
    print(f"\nValidation Results:\n{results}")