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

