import os
import platform
import re
from collections import Counter

def detect_os():
    return platform.system()

def find_log_files(os_name):
    log_files = []

    if os_name == "Windows":
        # Common log file directories on Windows
        windows_log_dirs = [
            os.getenv('SystemRoot', r'C:\Windows') + r'\System32\Winevt\Logs',
            os.getenv('SystemRoot', r'C:\Windows') + r'\Logs',
        ]
        for log_dir in windows_log_dirs:
            if os.path.exists(log_dir):
                for file in os.listdir(log_dir):
                    if file.endswith('.evtx'):  # Event log files
                        log_files.append(os.path.join(log_dir, file))
    elif os_name in ["Linux", "Darwin"]:
        # Common log file directories on Unix-based systems
        unix_log_dirs = ['/var/log']
        for log_dir in unix_log_dirs:
            if os.path.exists(log_dir):
                for file in os.listdir(log_dir):
                    log_files.append(os.path.join(log_dir, file))
    return log_files

def read_log_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.readlines()
    except Exception as e:
        return [str(e)]

def analyze_log_lines(lines):
    levels = ["INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"]
    level_counts = Counter()
    messages = []
    error_messages = []

    for line in lines:
        for level in levels:
            if level in line:
                level_counts[level] += 1
                messages.append(line.strip())
                if level in ["ERROR", "CRITICAL"]:
                    error_messages.append(line.strip())
                break

    return level_counts, messages, error_messages

def generate_summary(level_counts, messages, error_messages):
    total_entries = sum(level_counts.values())
    summary = []

    if total_entries == 0:
        return "No significant log entries found."

    summary.append(f"A total of {total_entries} log entries were found.")

    if level_counts["ERROR"] > 0 or level_counts["CRITICAL"] > 0:
        summary.append(f"There are {level_counts['ERROR']} error entries and {level_counts['CRITICAL']} critical entries.")
        if error_messages:
            summary.append("Some of the critical errors are:")
            for msg in error_messages[:5]:
                summary.append(f"  - {msg}")
    else:
        summary.append("No critical or error entries found.")

    common_messages = Counter(messages).most_common(5)
    if common_messages:
        summary.append("Some of the most common log entries are:")
        for msg, count in common_messages:
            summary.append(f"  - {msg} (occurred {count} times)")

    return "\n".join(summary)

def summarize_log_file(file_path):
    lines = read_log_file(file_path)
    if lines and "Permission denied" in lines[0]:
        return "Permission denied. Try running with elevated privileges."

    level_counts, messages, error_messages = analyze_log_lines(lines)
    return generate_summary(level_counts, messages, error_messages)

def main():
    os_name = detect_os()
    print(f"Detected OS: {os_name}")

    log_files = find_log_files(os_name)

    if not log_files:
        print("No log files found.")
        return

    for log_file in log_files:
        print(f"Analyzing log file: {log_file}")
        summary = summarize_log_file(log_file)
        print(f"Summary of {log_file}:\n{summary}\n")

if __name__ == "__main__":
    main()
