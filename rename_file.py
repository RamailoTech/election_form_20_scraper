import os
import re

# Specify the directory containing the files
directory = "results/Parsed_Pdfs/Chhattisgarh/AE_2023"  # Update this with the path to your folder

# Define the regex pattern to match the original filenames
pattern = r'^JSON_chhattisgarh_2023_AC_AC(\d+)Form\d+\.json$'

# Iterate over all files in the directory
for filename in os.listdir(directory):
    original_path = os.path.join(directory, filename)
    
    # Check if the file matches the specified pattern
    if re.match(pattern, filename):
        # Extract the numeric part (e.g., '68') from the filename using regex
        match = re.match(pattern, filename)
        if match:
            numeric_part = match.group(1)  # Extract the numeric part (\d+)
            
            # Construct the new filename
            new_filename = f"JSON_chhattisgarh_2023_AC_{numeric_part}.json"
            new_path = os.path.join(directory, new_filename)
            
            # Rename the file
            try:
                os.rename(original_path, new_path)
                print(f"Renamed '{original_path}' to '{new_path}'")
            except Exception as e:
                print(f"Error renaming '{original_path}': {e}")
    else:
        print(f"Skipped '{original_path}' (filename does not match the pattern)")

print("File renaming completed.")
