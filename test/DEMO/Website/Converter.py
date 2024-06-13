import pandas as pd

# Load the file content with the correct encoding
file_path = '/Users/harsha/Desktop/Linux_System_Logs.txt'
with open(file_path, 'r', encoding='ISO-8859-1') as file:
    log_data = file.readlines()

# Initialize lists for each column
month = []
date = []
timestamp = []
hostname = []
process = []
log_message = []

# Process each line in the log file
for line in log_data:
    parts = line.split()
    if len(parts) > 5:
        month.append(parts[0])
        date.append(parts[1])
        timestamp.append(parts[2])
        hostname.append(parts[3])
        # Check if there's a colon to determine the end of process name
        if ': ' in line:
            proc_start = line.index(parts[4])
            proc_end = line.index(': ', proc_start)
            process.append(line[proc_start:proc_end])
            log_message.append(line[proc_end + 2:].strip())
        else:
            process.append(parts[4])
            log_message.append(" ".join(parts[5:]))

# Create a DataFrame from the lists
df = pd.DataFrame({
    'Month': month,
    'Date': date,
    'Timestamp': timestamp,
    'Hostname': hostname,
    'Process': process,
    'LogMessage': log_message
})

# Save to CSV
output_path = '/Users/harsha/Desktop/dataset_Logs.csv'
df.to_csv(output_path, index=False)
