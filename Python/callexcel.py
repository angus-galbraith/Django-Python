import os

# Define the full path to your Excel file
file_path = "/Users/angusgalbraith/Library/CloudStorage/OneDrive-Personal/Programming/Python/Darts/darts.xlsx"  # Replace with the actual path

# Construct the shell command to open the file with Microsoft Excel
# The 'open -a' command specifies the application, and the single quotes handle spaces in the path
command = f"open -a 'Microsoft Excel.app' '{file_path}'"

# Execute the command
os.system(command)