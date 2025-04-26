import os  # Import the os module to interact with the operating system

# === Configuration ===
TARGET_EXTENSIONS = ('.txt', '.docx', '.jpg')  # Define the target file types we want to search for

# === Input ===
directory = input("Enter the path of the directory to search in: ")  # Ask the user for the directory path

# === List to collect found files ===
found_files = []  # Create an empty list to store the full paths of matching files

# === File Search ===
for root, dirs, files in os.walk(directory):  # Walk through all folders and files starting from the user directory
    for file in files:  # Loop through each file in the current folder
        if file.lower().endswith(TARGET_EXTENSIONS):  # Check if the file has one of the target extensions
            full_path = os.path.join(root, file)  # Create the full file path
            found_files.append(full_path)  # Add the file path to the list

# === Save Results to a Log File ===
with open("files.log", "w") as log:  # Open (or create) a file called 'files.log' to write the results
    for file_path in found_files:  # Loop through all found file paths
        log.write(file_path + "\n")  # Write each file path on a new line

print(f"\n{len(found_files)} files found. Saved to 'files.log'.")  # Print a message showing how many files were found
