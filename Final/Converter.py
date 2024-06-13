import platform
import os
import pandas as pd
from PyPDF2 import PdfFileReader


# Function to detect the operating system automatically
def detect_os():
    os_name = platform.system()
    if os_name == "Darwin":
        return "macOS"
    elif os_name == "Linux":
        return "Linux"
    elif os_name == "Windows":
        return "Windows"
    else:
        raise Exception("Unsupported Operating System")


# Function to allow user to select the operating system manually
def select_os_manually():
    print("Select your operating system:")
    print("1. macOS")
    print("2. Linux")
    print("3. Windows")
    choice = input("Enter your choice (1/2/3): ")
    if choice == '1':
        return "macOS"
    elif choice == '2':
        return "Linux"
    elif choice == '3':
        return "Windows"
    else:
        print("Invalid choice. Detecting OS automatically.")
        return detect_os()


# Read log or text file
def read_log_file(file_path):
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        return file.readlines()


# Read PDF file
def read_pdf_file(file_path):
    content = ""
    with open(file_path, 'rb') as file:
        reader = PdfFileReader(file)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            content += page.extract_text()
    return content.split('\n')


# Parse log lines into a structured format with specific column names
def parse_log_lines(log_lines, os_type):
    data = []
    if os_type == "macOS":
        for line in log_lines:
            parts = line.split()
            entry = {
                'Month': parts[0] if len(parts) > 0 else None,
                'Date': parts[1] if len(parts) > 1 else None,
                'Time': parts[2] if len(parts) > 2 else None,
                'Hostname': parts[3] if len(parts) > 3 else None,
                'Operating System': 'macOS',
                'Source': parts[4].rstrip(':') if len(parts) > 4 else None,
                'Severity Level': parts[5] if len(parts) > 5 else None,
                'Message Content': ' '.join(parts[6:]) if len(parts) > 6 else None
            }
            data.append(entry)
    elif os_type == "Linux":
        for line in log_lines:
            parts = line.split()
            if len(parts) >= 5:
                severity_level = parts[4] if parts[4] in ["INFO", "WARN", "ERROR", "CRITICAL"] else ''
                message_content = ' '.join(parts[5:]) if severity_level else ' '.join(parts[4:])
                entry = {
                    'Month': parts[0],
                    'Date': parts[1],
                    'Time': parts[2],
                    'Hostname': parts[3],
                    'Operating System': 'Linux',
                    'Source': parts[4].rstrip(':') if not severity_level else '',
                    'Severity Level': severity_level,
                    'Message Content': message_content
                }
                data.append(entry)
    elif os_type == "Windows":
        for line in log_lines:
            parts = line.split(',')
            if len(parts) >= 4:
                date_time_parts = parts[0].split()
                date_parts = date_time_parts[0].split('-')
                entry = {
                    'Month': date_parts[1],
                    'Date': date_parts[2],
                    'Year': date_parts[0],
                    'Time': date_time_parts[1] if len(date_time_parts) > 1 else '',
                    'Hostname': parts[1],
                    'Operating System': 'Windows',
                    'Source': parts[2],
                    'Severity Level': parts[3],
                    'Message Content': ','.join(parts[4:])
                }
                data.append(entry)
    return data


# Main function to integrate all parts
def main(input_file, output_file, os_type):
    if input_file.endswith('.csv'):
        print("The input file is already in CSV format. No conversion needed.")
        return
    elif input_file.endswith('.xlsx'):
        print("The input file is already in Excel format. No conversion needed.")
        return

    if input_file.endswith('.log') or input_file.endswith('.txt'):
        log_lines = read_log_file(input_file)
    elif input_file.endswith('.pdf'):
        log_lines = read_pdf_file(input_file)
    else:
        raise Exception("Unsupported file type")

    data = parse_log_lines(log_lines, os_type)

    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    print(f"Output saved to {output_file}")


# Allow user to select the operating system manually or detect it automatically
print("Select how you want to choose the operating system:")
print("1. Detect automatically")
print("2. Choose manually")
choice = input("Enter your choice (1/2): ")

if choice == '1':
    os_type = detect_os()
elif choice == '2':
    os_type = select_os_manually()
else:
    print("Invalid choice. Detecting OS automatically.")
    os_type = detect_os()

# Example usage:
input_file = input("Enter the path to your log file: ")  # Replace with the path to your log file
output_file = "output.xlsx"  # Name of the output Excel file
main(input_file, output_file, os_type)
