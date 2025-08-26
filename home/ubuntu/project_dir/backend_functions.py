# backend_functions.py - Improved and Complete Version with Sync Fix

import csv
import os
import datetime
import tempfile
import shutil
import hashlib

# Configuration: Define file paths and Fieldnames
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITIZENS_CSV_FILE = os.path.join(BASE_DIR, "citizens_data.csv")
ADMINS_CSV_FILE = os.path.join(BASE_DIR, "admins_data.csv")
AID_HISTORY_CSV_FILE = os.path.join(BASE_DIR, "aid_history.csv")
MESSAGES_CSV_FILE = os.path.join(BASE_DIR, "messages.csv")
ID_COUNTER_FILE = os.path.join(BASE_DIR, "citizen_id_counter.txt")

# Define the exact headers/fieldnames for CSV files
CITIZENS_FIELDNAMES = [
    "id", "national_id", "full_name", "date_of_birth", "phone_number", 
    "address", "household_members", "dependents", "needs_description", 
    "priority_score", "is_active", "registration_date", "secret_code_hash"
]

ADMINS_FIELDNAMES = [
    "id", "username", "password_hash", "full_name", "organization_id", "role"
]

AID_HISTORY_FIELDNAMES = [
    "id", "citizen_internal_id", "entry_type", "date", "next_date", "timestamp"
]

MESSAGES_FIELDNAMES = [
    "id", "citizen_internal_id", "message", "timestamp"
]

# ---------------------------- PASSWORD HASHING ----------------------------
def _hash_password(password):
    salt = "citizen_aid_system_2024"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

# ---------------------------- ID SYNC FUNCTIONS ----------------------------
def update_citizen_id_counter(new_value):
    """Updates the citizen_id_counter.txt file with a new value."""
    try:
        with open(ID_COUNTER_FILE, "w") as f:
            f.write(str(new_value))
    except IOError as e:
        print(f"Warning: Could not update {ID_COUNTER_FILE}: {e}")

def sync_citizen_id_counter():
    """Synchronizes the counter file with the max ID from citizens_data.csv."""
    if os.path.exists(CITIZENS_CSV_FILE):
        try:
            import pandas as pd
            df = pd.read_csv(CITIZENS_CSV_FILE)
            if not df.empty and "id" in df.columns:
                max_id = df["id"].astype(int).max()
                update_citizen_id_counter(int(max_id) + 1)
        except Exception as e:
            print(f"Warning: Could not sync citizen ID counter: {e}")
# ---------------------------- CSV FUNCTIONS ----------------------------
def read_csv_dict(file_path, fieldnames):
    try:
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield {field: row.get(field, "") for field in fieldnames}
    except FileNotFoundError:
        print(f"Info: File not found {file_path}. Returning empty data.")
        return
    except Exception as e:
        print(f"Error reading CSV {file_path}: {e}")
        return

def append_csv_dict(file_path, data_dict, fieldnames):
    file_exists = os.path.isfile(file_path) and os.path.getsize(file_path) > 0
    try:
        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL, extrasaction='ignore')
            if not file_exists:
                writer.writeheader()
            row_to_write = {field: data_dict.get(field, "") for field in fieldnames}
            writer.writerow(row_to_write)
        return True
    except IOError as e:
        print(f"Error appending to CSV {file_path}: {e}")
        return False

def overwrite_csv_dict(file_path, list_of_dicts, fieldnames):
    temp_file_path = None
    try:
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        temp_fd, temp_file_path = tempfile.mkstemp(dir=os.path.dirname(file_path) or ".", prefix=os.path.basename(file_path) + ".tmp")
        with os.fdopen(temp_fd, "w", newline="", encoding="utf-8") as temp_f:
            writer = csv.DictWriter(temp_f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL, extrasaction='ignore')
            writer.writeheader()
            writer.writerows([{field: d.get(field, "") for field in fieldnames} for d in list_of_dicts])
        shutil.move(temp_file_path, file_path)
        return True
    except Exception as e:
        print(f"Error overwriting CSV {file_path}: {e}")
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except OSError:
                pass
        return False
# ---------------------------- ID GENERATION ----------------------------
def get_next_citizen_id_csv():
    max_id = 0
    try:
        existing_ids = []
        for citizen in read_csv_dict(CITIZENS_CSV_FILE, CITIZENS_FIELDNAMES):
            try:
                citizen_id = int(citizen.get("id", 0))
                existing_ids.append(citizen_id)
            except (ValueError, TypeError):
                continue
        if existing_ids:
            max_id = max(existing_ids)
        else:
            if os.path.exists(ID_COUNTER_FILE):
                with open(ID_COUNTER_FILE, "r") as f:
                    content = f.read().strip()
                    if content:
                        counter_val = int(content)
                        if counter_val > max_id:
                            max_id = counter_val - 1
    except Exception:
        max_id = 0

    next_id = max_id + 1
    try:
        os.makedirs(os.path.dirname(ID_COUNTER_FILE) or ".", exist_ok=True)
        with open(ID_COUNTER_FILE, "w") as f:
            f.write(str(next_id))
    except IOError as e:
        print(f"Warning: Could not update {ID_COUNTER_FILE}: {e}")
    return next_id

def get_next_id_for_table(csv_file, fieldnames):
    max_id = 0
    try:
        for row in read_csv_dict(csv_file, fieldnames):
            try:
                row_id = int(row.get("id", 0))
                if row_id > max_id:
                    max_id = row_id
            except (ValueError, TypeError):
                continue
    except Exception:
        pass
    return max_id + 1
# ---------------------------- SETUP CSV FILES ----------------------------
def setup_csv_files():
    files_to_setup = {
        CITIZENS_CSV_FILE: CITIZENS_FIELDNAMES,
        ADMINS_CSV_FILE: ADMINS_FIELDNAMES,
        AID_HISTORY_CSV_FILE: AID_HISTORY_FIELDNAMES,
        MESSAGES_CSV_FILE: MESSAGES_FIELDNAMES
    }

    for file_path, fieldnames in files_to_setup.items():
        if not os.path.isfile(file_path):
            try:
                os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                print(f"Created {file_path} with headers: {fieldnames}")
            except IOError as e:
                print(f"Error creating {file_path}: {e}")
    
    if not os.path.exists(ID_COUNTER_FILE):
        try:
            with open(ID_COUNTER_FILE, "w") as f:
                f.write("0")
            print(f"Created and initialized {ID_COUNTER_FILE}")
        except IOError as e:
            print(f"Error creating {ID_COUNTER_FILE}: {e}")

    sync_citizen_id_counter()
    print("CSV File setup check complete.")

# ---------------------------- AUTH FUNCTIONS ----------------------------
def verify_admin_login_csv(username, password):
    password_hash = _hash_password(password)
    for admin in read_csv_dict(ADMINS_CSV_FILE, ADMINS_FIELDNAMES):
        if admin.get("username") == username and admin.get("password_hash") == password_hash:
            return admin
    return None

def verify_citizen_login_csv(national_id, secret_code):
    provided_hash = _hash_password(secret_code)
    for citizen in read_csv_dict(CITIZENS_CSV_FILE, CITIZENS_FIELDNAMES):
        is_active = str(citizen.get("is_active", "True")).strip().lower() == "true"
        if (
            citizen.get("national_id") == national_id and 
            citizen.get("secret_code_hash") == provided_hash and
            is_active
        ):
            try:
                citizen["id"] = int(citizen["id"])
                citizen["priority_score"] = float(citizen.get("priority_score", 0.0))
                citizen["household_members"] = int(citizen.get("household_members", 0))
                citizen["dependents"] = int(citizen.get("dependents", 0))
                citizen["is_active"] = True
                if "secret_code_hash" in citizen:
                    del citizen["secret_code_hash"]
            except (ValueError, TypeError):
                pass
            return citizen
    return None
# ---------------------------- REGISTRATION FUNCTIONS ----------------------------
def check_citizen_exists_csv(national_id):
    for citizen in read_csv_dict(CITIZENS_CSV_FILE, CITIZENS_FIELDNAMES):
        if citizen.get("national_id") == national_id:
            return True
    return False

def register_citizen_csv(citizen_data):
    if "national_id" not in citizen_data or "secret_code" not in citizen_data or "full_name" not in citizen_data:
        print("Error: Required fields missing.")
        return None
    if check_citizen_exists_csv(citizen_data["national_id"]):
        print("Error: Citizen already exists.")
        return None

    new_id = get_next_citizen_id_csv()
    if new_id is None:
        print("Error: Could not generate citizen ID.")
        return None

    secret_hash = _hash_password(citizen_data["secret_code"])
    new_record = {
        "id": str(new_id),
        "national_id": citizen_data["national_id"],
        "full_name": citizen_data["full_name"],
        "date_of_birth": citizen_data.get("date_of_birth", ""),
        "phone_number": citizen_data.get("phone_number", ""),
        "address": citizen_data.get("address", ""),
        "household_members": str(citizen_data.get("household_members", 0)),
        "dependents": str(citizen_data.get("dependents", 0)),
        "needs_description": citizen_data.get("needs_description", ""),
        "priority_score": str(citizen_data.get("priority_score", 0.0)),
        "is_active": "True",
        "registration_date": datetime.datetime.now().isoformat(),
        "secret_code_hash": secret_hash
    }

    if append_csv_dict(CITIZENS_CSV_FILE, new_record, CITIZENS_FIELDNAMES):
        print(f"Citizen registered with ID: {new_id}")
        del new_record["secret_code_hash"]
        return new_record
    else:
        return None

def register_admin_csv(username, password, full_name="", organization_id="", role="admin"):
    for admin in read_csv_dict(ADMINS_CSV_FILE, ADMINS_FIELDNAMES):
        if admin.get("username") == username:
            print(f"Admin '{username}' already exists.")
            return False

    new_id = get_next_id_for_table(ADMINS_CSV_FILE, ADMINS_FIELDNAMES)
    password_hash = _hash_password(password)
    new_admin = {
        "id": str(new_id),
        "username": username,
        "password_hash": password_hash,
        "full_name": full_name,
        "organization_id": organization_id,
        "role": role
    }
    return append_csv_dict(ADMINS_CSV_FILE, new_admin, ADMINS_FIELDNAMES)

# ---------------------------- MAIN ----------------------------
if __name__ == "__main__":
    setup_csv_files()
    print("Backend is ready and ID counter synced.")
def get_citizens_list_csv():
    """Returns a list of all citizens from the CSV."""
def get_citizens_list_csv(filter_type=None, sort_by=None):
    """Returns a list of citizens, optionally filtered and sorted."""
    all_citizens = list(read_csv_dict(CITIZENS_CSV_FILE, CITIZENS_FIELDNAMES))

    if filter_type == "received":
        all_citizens = [c for c in all_citizens if float(c.get("priority_score", 0)) > 0]
    elif filter_type == "not_received":
        all_citizens = [c for c in all_citizens if float(c.get("priority_score", 0)) == 0]

    if sort_by and sort_by in CITIZENS_FIELDNAMES:
        try:
            all_citizens.sort(key=lambda x: x.get(sort_by))
        except Exception as e:
            print(f"Sorting failed: {e}")

    return all_citizens



def save_aid_history_entry(citizen_internal_id, entry_type, date_str, next_date_str=""):
    """Saves an aid history entry for a citizen."""
    new_id = get_next_id_for_table(AID_HISTORY_CSV_FILE, AID_HISTORY_FIELDNAMES)
    record = {
        "id": str(new_id),
        "citizen_internal_id": str(citizen_internal_id),
        "entry_type": entry_type,
        "date": date_str,
        "next_date": next_date_str,
        "timestamp": datetime.datetime.now().isoformat()
    }
    return append_csv_dict(AID_HISTORY_CSV_FILE, record, AID_HISTORY_FIELDNAMES)

def save_message_entry(citizen_internal_id, message):
    """Saves a message entry for a citizen."""
    new_id = get_next_id_for_table(MESSAGES_CSV_FILE, MESSAGES_FIELDNAMES)
    record = {
        "id": str(new_id),
        "citizen_internal_id": str(citizen_internal_id),
        "message": message,
        "timestamp": datetime.datetime.now().isoformat()
    }
    return append_csv_dict(MESSAGES_CSV_FILE, record, MESSAGES_FIELDNAMES)

def check_citizen_received_aid(citizen_internal_id):
    """Checks if a citizen has received aid (i.e., has an aid history entry with no next_date)."""
    for entry in read_csv_dict(AID_HISTORY_CSV_FILE, AID_HISTORY_FIELDNAMES):
        if entry.get("citizen_internal_id") == str(citizen_internal_id) and entry.get("next_date") == "":
            return True
    return False

def get_citizen_details_csv(internal_id):
    """Retrieves a single citizen's details by their internal ID."""
    for citizen in read_csv_dict(CITIZENS_CSV_FILE, CITIZENS_FIELDNAMES):
        if citizen.get("id") == str(internal_id):
            try:
                citizen["id"] = int(citizen["id"])
                citizen["priority_score"] = float(citizen.get("priority_score", 0.0))
                citizen["household_members"] = int(citizen.get("household_members", 0))
                citizen["dependents"] = int(citizen.get("dependents", 0))
                citizen["is_active"] = str(citizen.get("is_active", "True")).strip().lower() == "true"
                if "secret_code_hash" in citizen:
                    del citizen["secret_code_hash"]
            except (ValueError, TypeError):
                pass
            return citizen
    return None

def update_citizen_details_csv(internal_id, updated_data):
    """Updates a citizen's details in the CSV file."""
    all_citizens = list(read_csv_dict(CITIZENS_CSV_FILE, CITIZENS_FIELDNAMES))
    updated = False
    for i, citizen in enumerate(all_citizens):
        if citizen.get("id") == str(internal_id):
            for key, value in updated_data.items():
                if key in CITIZENS_FIELDNAMES and key != "id": # Don't allow changing ID
                    if key == "priority_score":
                        all_citizens[i][key] = str(float(value))
                    elif key in ["household_members", "dependents"]:
                        all_citizens[i][key] = str(int(value))
                    else:
                        all_citizens[i][key] = value
            updated = True
            break
    if updated:
        return overwrite_csv_dict(CITIZENS_CSV_FILE, all_citizens, CITIZENS_FIELDNAMES)
    return False

def read_aid_history(citizen_internal_id=None):
    """Reads aid history, optionally filtered by citizen ID."""
    history = []
    for entry in read_csv_dict(AID_HISTORY_CSV_FILE, AID_HISTORY_FIELDNAMES):
        if citizen_internal_id is None or entry.get("citizen_internal_id") == str(citizen_internal_id):
            history.append(entry)
    return history

def read_messages(citizen_internal_id=None):
    """Reads messages, optionally filtered by citizen ID."""
    messages = []
    for msg in read_csv_dict(MESSAGES_CSV_FILE, MESSAGES_FIELDNAMES):
        if citizen_internal_id is None or msg.get("citizen_internal_id") == str(citizen_internal_id):
            messages.append(msg)
    return messages


