# PDF Processing Workflow

This document outlines the workflow for downloading PDFs, parsing them into JSON format using Azure's Form Recognizer, and converting the resulting JSON files into Excel spreadsheets.

## Downloading PDFs

### Requirements
- **Inputs**: 
  - State name
  - Election year
  - Constituency type
- **URL**: 
  - Valid URL corresponding to the state, election year, and constituency type.
- **Location**: 
  - The script must be executed from within India to access certain websites.

### Assumptions
- **URL Validity**: 
  - The specified URLs for downloading PDFs are assumed to be valid and accessible during execution.
- **Website Consistency**: 
  - The structure of target websites is expected to remain unchanged, including links and file formats.
- **PDF Accessibility**: 
  - It is assumed that the PDFs are publicly accessible without the need for authentication.
- **Input Accuracy**: 
  - Users are expected to input the correct state name, election year, and constituency type.

## Parsing PDFs to JSON

### Requirements
- **Azure Subscription**: 
  - An Azure subscription with access to the Form Recognizer service.
- **API Access**: 
  - A valid endpoint and API key for the Azure Form Recognizer.
- **Output**: 
  - PDF files downloaded from the specified websites.

### Assumptions
- **PDF Validity**: 
  - The PDF files are assumed to be well-formed and suitable for analysis by Azure's Form Recognizer.
- **Service Availability**: 
  - The Azure Form Recognizer service is expected to be operational during execution.
- **API Credentials**: 
  - The provided API key and endpoint are assumed to be valid and have necessary permissions.
- **JSON Structure**: 
  - The JSON output from the Form Recognizer is expected to be consistent and valid for further processing.
- **File Naming**: 
  - All relevant PDF files are assumed to have the `.pdf` extension.

## Converting JSON to Excel

### Requirements
- Presence of JSON files corresponding to the specified year, state, and constituency type in the designated folder.
- Input JSON files must contain a "tables" key.
- JSON files with the "tables" key should have the required structure.

### Assumptions
- **File Structure**: 
  - JSON files are organized in a directory structure based on state name, election year, and constituency type.
- **Data Consistency**: 
  - JSON files are expected to contain a "tables" key with relevant data.
- **Column Naming**: 
  - The first table in the JSON is assumed to have valid column headers; otherwise, it defaults to "Unnamed."
- **Data Cleaning**: 
  - The cleaning process assumes that unwanted characters can be safely removed, without preserving specific formatting.
- **Row Count**: 
  - The data in the JSON is expected to have a maximum row count specified.

## Additional Notes Fom KT discusion with palistha

- Understanding the conversion process from JSON to Excel is crucial, as it assumes that the higher row count contains the column headings.
- Different methods are employed when downloading PDFs based on state name, election year, and constituency type.
- Ensure that a VPN is active, as some URLs require that the connection appears to be from India.

## Name Mapping

### Requirements:
- **Inputs:** The function should accept the following inputs:
  - State name
  - Election year
  - Constituency type

- **File Input:** The input files are the json files that are generated using Azure from generated pdfs.

- **File Name Pattern:** The input file name should match the following pattern:
  - `"JSON_([A-Z]+)_(\d{4})_([A-Z]+)_(\d{3}).json"`
    - `[A-Z]+` corresponds to the state name and constituency type.
    - `\d{4}` corresponds to the election year.
    - `\d{3}` corresponds to a number that appears after the last underscore in the filename.

- **"Tables" Key in JSON:** Each JSON file should contain a `"tables"` key with the relevant data.

- **Output Directory:** The output of the mapping should be saved inside a `data_mapping` folder located within the `data` folder. If this folder does not exist, it must be created.

### Assumptions:
- **File Structure:** JSON files are organized in a directory structure as follows:
  - `data/<state_name>/<election_year>/<constituency_type>/`

- **Data Consistency:** Each JSON file is expected to follow a specific structure and contain a `"tables"` key.

- **File Name Consistency:** The input JSON file names are expected to conform to the pattern described above, and the last portion of the name (after the final underscore) is always a number (`\d{3}`).

- **Folder Existence:** The folder `data_mapping` inside the `data` directory is assumed to exist. If it doesn't, it should be created automatically by the system.

## Clean Data

### Requirements:
- Input files are the excel files that are generated from the json files.
- Ensure that CSV files for elections (e.g., `Maharashtra_AE.csv`, `Maharashtra_GA.csv`) are in the correct data directory.
- Ensure that JSON files (e.g., `maharastra_2019_AE.json`, `maharastra_2019_GA.json`) are in the `output/name_mappings/` directory.
- Provide the state name, election year, and constituency type (e.g., AE or GA) as command-line arguments. The script will not run if any of these parameters are missing or incorrect.
- Verify that the `data`, `output`, and `logs` directories exist, and create the `logs` and `output` directories if they do not exist.
- Check Excel file contents for correct formatting (e.g., number of columns).

### Assumptions:
- **Presence of Data Files:** The required CSV and JSON files exist in their specified directories.
- **Command-Line Arguments:** The script depends on three command-line arguments: state name, election year, and constituency type.
- **Excel File Directory Structure:** The Excel files to be processed are located in the specified directory structure.
- **Directory Existence:** The `data`, `output`, and `logs` directories either already exist or will be created by the script.
- **Data Format:** The input data in the Excel and CSV files is expected to be correctly formatted and clean.
- **File Naming Conventions:** The file names follow specific patterns for proper identification and processing.

## Issues Identified

### Filename Pattern Mismatch
- **Issue:** The pattern used to match names does not always match the names of the files created.
- **Impact:** This can cause problems in finding or processing the files correctly.

### Nested JSON Key Retrieval
- **Issue:** Sometimes, the `tables` key is nested within other keys in the JSON data, making it hard to find.
- **Proposed Solution:** Create a function to search through all levels of the JSON data to find the `tables` key no matter where it is located.

### Filename Pattern Conversion Error
- **Issue:** The system tries to convert filename patterns into numbers, but filenames can have letters as well, which causes errors.
- **Impact:** This prevents correct comparison and processing of filenames that include letters.
- **Proposed Solution:** Change the logic to handle filenames with letters without trying to convert them to numbers.
