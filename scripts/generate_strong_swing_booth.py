import os
import pandas as pd
from functools import reduce
import sys

# Function to append text to a file
def append_text_to_file(filename, text):
    """Function to append error message to log file.

    Args:
        filename (str): Name of the log file
        text (str): Log message"""
    if not os.path.exists(filename):
        with open(filename, "a") as file:
            file.write(text + "\n")
    else:
        with open(filename, "a") as file:
            file.write(text + "\n")

def get_election_df(constituency_type,state_name):
    if state_name == 'CH':
        election_df = pd.read_csv('data/CH_2023_namemapping.csv')
        
    if constituency_type == 'GA' and state_name == "MH":
        election_df = pd.read_csv('data/Maharashtra_GA.csv')
        
    if constituency_type == "AE" and state_name == "MH":
        election_df = pd.read_csv('data/Maharashtra_AE.csv') 
        
    return election_df




def generate_swing_and_strong_booths_df(AC, years, excel_dir):
    # Prepare to collect the file paths
    excel_files = []
    for dirpath, dirnames, filenames in os.walk(excel_dir):
        for year in years:
            if os.path.basename(dirpath) == year:  # Checking directory names against the specified years
                for filename in filenames:
                    if filename == f"{AC}.xlsx":  # Looking for specific Excel files
                        full_path = os.path.join(dirpath, filename)
                        excel_files.append(full_path)

    # Reading and merging Excel files
    merged_dfs = []
    for excel_file in excel_files:
        df = pd.read_excel(excel_file)
        year = os.path.basename(os.path.dirname(excel_file))  # Assuming folder names are the years
        if 'INC_Status' in df.columns:
            df.rename(columns={'INC_Status': year}, inplace=True)
        df.dropna(subset=['SN'], inplace=True)
        df['SN'] = df['SN'].astype(int)
        if year in df.columns:  # Check if the 'year' column was successfully added
            merged_dfs.append(df[['SN', year]])

    # Use reduce to merge all dataframes on 'SN' using an outer join, with an initial value in case of an empty list
    if len(merged_dfs):
        merged_df = reduce(lambda left, right: pd.merge(left, right, on='SN', how='outer'), merged_dfs)
    else:
        return pd.DataFrame(), pd.DataFrame()  # Return empty DataFrames if no files were processed

    # Keeping only the columns for 'SN' and the specified years
    valid_years = [year for year in years if year in merged_df.columns]
    required_columns = ['SN'] + valid_years
    merged_df = merged_df[required_columns]

    # Generating strong and swing DataFrames
    if valid_years:  # Only process if there are valid year columns
        conditions_won = [merged_df[year] == 'WON' for year in valid_years]
        strong_df = merged_df[reduce(lambda x, y: x & y, conditions_won)]
        swing_df = merged_df[reduce(lambda x, y: x | y, conditions_won)]
    else:
        strong_df = pd.DataFrame()  # Empty DataFrame if no valid year columns
        swing_df = pd.DataFrame()  # Empty DataFrame if no valid year columns

    return swing_df, strong_df


def create_strong_and_swing_and_dump_excel_files(state_name, election_year, constituency_type):
    # excel_dir = f'data/intermediate_tables/{state_name}'
    excel_dir = f'results/intermediate_tables/{state_name}'
    #mention all the intermediate tables for the particular state
    years = ['AE_2014', 'GE_2014', '2019'] 
    ACS = 288
    output_dir = f'output/strong_and_swing_booths/{state_name}' 
    log_file_name = f'logs/{state_name}_{election_year}_{constituency_type}_strong_swing_booths.txt'
    for i in range(1, ACS+1):
        try: 
            swing_df, strong_df = generate_swing_and_strong_booths_df(i, years, excel_dir)
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            strong_file_path = f"{output_dir}/{i}_strong.xlsx"
            strong_df.to_excel(strong_file_path, index=False)
            
            swing_file_path = f"{output_dir}/{i}_swing.xlsx"
            swing_df.to_excel(swing_file_path, index=False)

        except Exception as exc: 
            append_text_to_file(log_file_name,f"Error processing file: {i} - {exc}\n")
            continue
        



def main():
    # Check if the required arguments are provided
    if len(sys.argv) < 4:
        print("Usage: python json_to_excel.py <state_name> <election_year> <constituency_type>")
        sys.exit(1)

    # Get the arguments from the command line
    state_name = sys.argv[1]
    election_year = sys.argv[2]
    constituency_type = sys.argv[3]

    # Call the function to process the JSON files
    create_strong_and_swing_and_dump_excel_files(state_name, election_year, constituency_type)

if __name__ == "__main__":
    main()
