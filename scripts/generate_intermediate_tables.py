import os
import pandas as pd
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


def get_election_df(type):
    if type == 'AE':
        election_df = pd.read_csv('data/Maharashtra_AE.csv')
    if type == 'GA':
        election_df = pd.read_csv('data/Maharashtra_GA.csv')
        
    return election_df



def get_parties(year,AC,constituency_type):
    election_df = get_election_df(constituency_type)
    top_3 = [1,2,3]
    # Define conditions
    condition_general = (
        (election_df['Year'] == year) &
        (election_df['Constituency_No'] == AC) &
        (~election_df['Candidate'].isin(['None of the Above', 'NOTA']))
    )

    condition_inc = (
        (election_df['Party'] == 'INC')
    )

    # Use bitwise OR to combine conditions
    filtered_election_df = election_df[
        (condition_general & election_df['Position'].isin(top_3)) |
        (condition_inc & condition_general)
    ]
    
    return filtered_election_df.sort_values(by='Position', ascending=True)['Party'].tolist()



def intermediate_table(df, year,constituency_type):
    constituency = df.iloc[0]["Constituency"]
    year = df.iloc[0]["Year"]

    parties_ordered = get_parties(year, constituency,constituency_type)

    # Filter the columns that contains parties_ordered and col_ and 'NOTA'
    col_columns = [
        col
        for col in df.columns
        if col in parties_ordered or col.startswith("col_") or col == "NOTA"
    ]

    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [
            dup + "_" + str(i) if i != 0 else dup for i in range(sum(cols == dup))
        ]
    df.columns = cols

    # Add INC Status Column
    max_votes_column = df[col_columns].idxmax(axis=1)
    df["INC_Status"] = max_votes_column.map(lambda x: "WON" if x == "INC" else "LOSS")

    top_parties = parties_ordered[:3]

    for party in top_parties:
        df[f"{party} Share%"] = ((df[party] / df["Total"]) * 100).round(2)

    # Prepare the columns for the final DataFrame
    final_columns = (
        ["SN", "Constituency", "Year"]
        + [item for party in top_parties for item in (party, f"{party} Share%")]
        + ["Total", "INC_Status"]
    )
    final_df = df[final_columns]

    # delete rows where SN is null
    final_df = final_df[final_df["SN"].notnull()]

    return final_df, constituency


def create_intermediate_tables_and_dump_excel_files(
    state_name, election_year, constituency_type
):
    # excel_dir = f"data/cleaned_excel/{state_name}/{constituency_type}_{election_year}"
    excel_dir = f"output/cleaned_election_data/MH/2019_AE_valid"
    
    output_dir = (
        f"data/intermediate_tables/{state_name}/{constituency_type}_{election_year}"
    )
    log_file_name = f"logs/{state_name}_{election_year}_intermediate_tables_logs.txt"
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(excel_dir):
        if filename.endswith(".xlsx"):
            try:
                df = pd.read_excel(os.path.join(excel_dir, filename))
                intermediate_df, constituency = intermediate_table(df, election_year,constituency_type)
                output_file_path = os.path.join(output_dir, f"{constituency}.xlsx")
                intermediate_df.to_excel(output_file_path, index=False)
            except Exception as exc:
                append_text_to_file(
                    log_file_name, f"Error processing file: {filename} - {exc}\n"
                )
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
    create_intermediate_tables_and_dump_excel_files(state_name, election_year, constituency_type)

if __name__ == "__main__":
    main()


