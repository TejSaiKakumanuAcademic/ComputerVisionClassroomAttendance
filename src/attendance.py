import csv
import os
try:
    from utils import get_current_date
except ImportError:
    from src.utils import get_current_date

def log_attendance(results, log_file="../data/attendance_log.csv"):
    """
    Appends an array of face recognition results to the attendance log.
    An entry format: face_encoding, face_name, timestamp
    """
    # Adjust path if running from the root directory instead of src/
    if not os.path.exists(os.path.dirname(log_file)):
        if log_file.startswith("../"):
            possible_root_path = log_file[3:]
            if os.path.exists(os.path.dirname(possible_root_path) or "."):
                log_file = possible_root_path

    # Ensure the directory exists
    dir_name = os.path.dirname(log_file)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    file_exists = os.path.exists(log_file) and os.path.getsize(log_file) > 0

    with open(log_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['face_encoding', 'face_name', 'timestamp'])

        for res in results:
            name = res.get('name', 'Unknown')
            encoding = res.get('encoding')
            
            # Convert numpy array to list and then string to store in a single CSV column
            if encoding is not None:
                encoding_str = str(encoding.tolist())
            else:
                encoding_str = ''
                
            timestamp = get_current_date()
            writer.writerow([encoding_str, name, timestamp])
