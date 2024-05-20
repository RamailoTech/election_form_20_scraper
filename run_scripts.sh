#!/bin/bash

# Define paths to your Python scripts
download_pdfs="scripts/download_pdfs.py"
parse_json_script="scripts/pdf_to_json.py"
json_to_excel="scripts/json_to_excel.py"
name_mapping="scripts/name_mapping.py"
clean_excel="scripts/clean_excel.py"
intermediate_tables="scripts/generate_intermediate_tables.py"
string_and_swing_booth="scripts/generate_strong_swing_booth.py"

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <state_name> <election_year> <constituency_type>"
    exit 1
fi

# Assign the arguments to variables
state_name=$1
election_year=$2
constituency_type=$3

# Run each Python script with the specified parameters
echo "Running scripts for state: $state_name, year: $election_year, constituency type: $constituency_type..."
echo "Executing $download_pdfs..."
python3 "$download_pdfs" "$state_name" "$election_year" "$constituency_type"

echo "Executing $parse_json_script..."
python3 "$parse_json_script" "$state_name" "$election_year" "$constituency_type"

echo "Executing $json_to_excel..."
python3 "$json_to_excel" "$state_name" "$election_year" "$constituency_type"

echo "Executing $name_mapping..."
python3 "$name_mapping" "$state_name" "$election_year" "$constituency_type"

echo "Executing $clean_excel..."
python3 "$clean_excel" "$state_name" "$election_year" "$constituency_type"

echo "Executing $intermediate_tables..."
python3 "$intermediate_tables" "$state_name" "$election_year" "$constituency_type"

echo "Executing $string_and_swing_booth..."
python3 "$string_and_swing_booth" "$state_name" "$election_year" "$constituency_type"

echo "All scripts executed successfully."
