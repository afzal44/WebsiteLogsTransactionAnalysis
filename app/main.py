import re
import os
import json
import gzip
# import pandas as pd
import json
from helper import main_helper


# Function to parse logs from directory recursively
def parse_logs_recursively(path):
    print(f"{__name__}.parse_logs_recursively function invoked")
    mh = main_helper()
    transactions = []
    errors = []
    file_count = 0
    # Regular expressions for extracting timestamp and request_id
    timestamp_reg = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z"
    request_id_reg = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    # Regular expressions for extracting transaction details
    t_pattern = r"{transaction: ({(.*?)})}"
    f_pattern = r"sync {{([^:]+): (.*?)}"

    if os.path.isdir(path):
        print(f"Directory mode execution Started...")
        for root, dirs, files in os.walk(path):
            for file_name in files:
                file_count += 1
                if file_name.endswith('.gz') or file_name.endswith('.log'):
                    file_path = os.path.join(root, file_name)
                    if file_name.endswith('.gz'):
                        file = gzip.open(file_path, 'rb')
                        # print('*'*20,'\n',file_path,'\n','file count:',file_count)
                        data = [cl for cl in mh.make_complete_lines([f.decode('utf-8') for f in file.readlines()])]
                    elif file_name.endswith('.log'):
                        file = open(file_path, 'r')
                        data = [cl for cl in mh.make_complete_lines([f for f in file.readlines()])]
                    else:
                        msg = f"Cannot parse this file's extension: {file_name.split('.')[-1]}"
                        print(msg)
                        return msg
                    for line in data:
                        # Looking for timestamp
                        timestamp_match = re.search(timestamp_reg, line)
                        timestamp = timestamp_match.group() if timestamp_match else ""

                        # Looking for request id
                        request_id_match = re.search(request_id_reg, line)
                        request_id = request_id_match.group() if request_id_match else ""
                        transaction_data = mh.transactions_payload(line)
                        if transaction_data:
                            transaction_data["timestamp"] = timestamp
                            transaction_data["request_id"] = request_id
                            transactions.append(transaction_data)
                        if "ERROR" in line and not '/var/task' in line and 'lambdaHandler' not in line:
                            errors_data = mh.errors_payload(line)
                            if errors_data:
                                errors_data["timestamp"] = timestamp
                                errors_data["request_id"] = request_id
                                errors.append(errors_data)

    print(f"Total {file_count} log files processed.")
    # Convert dictionary to JSON

    json_t_data = json.dumps(transactions, indent=2)
    # Write JSON data to a file
    print(f"writing to transaction_data.json file...")
    with open(r'/app/reports/success_transaction_data.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_t_data)
    print(f"data written to transaction_data.json file... at {os.getcwd()} path ")

    # Convert dictionary to JSON
    json_e_data = json.dumps(errors, indent=2)
    # Write JSON data to a file
    print(f"writing to errors_data.json file...")
    with open(r'/app/reports/errors_data.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_e_data)
    print(f"data written to errors_data.json file... at {os.getcwd()} path ")

    return transactions, errors
# path = r'calo_balance_sync\app\test'
# Example usage
path = r"C:\Users\afjal\OneDrive\Desktop\big Data Engineer\calo_balance_sync\logs"
transactions, errors = parse_logs_recursively(path)
print(len(transactions))
print(len(errors))

# Create DataFrames
# transactions_df = pd.DataFrame(transactions)
# errors_df = pd.DataFrame(errors)