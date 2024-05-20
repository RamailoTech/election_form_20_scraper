## Election Data Processing

Welcome to the Election Data Processing repository! This project is designed to efficiently process, analyze, and visualize election data. Whether you are working with local, state, or national election results, this toolkit provides the necessary tools to handle the data with ease.

### Features

- Data Ingestion: Load election data from PDF. Manually rotate if the orentation of pdfs are not in proper order.

* Data Parsing: Parse the data using Azure service.

* Data Cleaning: Handle missing values, correct errors, and standardize formats.

* Data Analysis: Calculate key statistics, such as voter turnout and candidate performance.

### Installation

1. Clone the repository:
   `repo`

2. Navigate to the project directory:
   `cd foldername`

3. Create a virtual environment:
   `python3 -m venv venv`

4. Activate the virtual environment:
   `source venv/bin/activate`

5. Install dependencies:
   `pip install -r requirements.txt`

6. Create .env file and add azure credentials.

7. Run the bash script:

`./run_scripts.sh state_name election_year constituency_type`

Note: Replace state_name, election_year, constituency_type with the specific state/year you want to work for. (Eg: ./run_scripts.sh MH 2019 AE)
