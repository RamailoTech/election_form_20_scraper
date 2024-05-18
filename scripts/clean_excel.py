import pandas as pd
import numpy as np
import os
import re
import json
from fuzzywuzzy import fuzz


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
            
            
def get_election_df(constituency_type, state_name):

    if constituency_type == "GA" and state_name == "MH":
        election_df = pd.read_csv("data/Maharashtra_GA.csv")

    if constituency_type == "AE" and state_name == "MH":
        election_df = pd.read_csv("data/Maharashtra_AE.csv",low_memory=False)
    
    if constituency_type == "AE" and state_name == "KA":
        election_df = pd.read_csv("data/Karnataka_AE.csv")

    if constituency_type == "AE" and state_name == "CH":
        election_df = pd.read_csv("data/Chhattisgarh_AE.csv")
    
    if constituency_type == "AE" and state_name == "RJ":
        election_df = pd.read_csv("data/AE_RAJASTHAN.csv")

    return election_df

def get_name_mappings(year, type, state):

    # Construct the file path based on the inputs
  
    file_path = f"data/name_mappings/{state}_{year}_{type}.json"
    if file_path:
        return file_path
    else:
        print("No name mapping file found.")

            
def get_columns_details(year,state, type, AC):
   
    election_df = get_election_df(type,state)
    filtered_election_df = election_df[
        (election_df["Year"] == year)
        & (election_df["Constituency_No"] == AC)
        & (~election_df["Candidate"].isin(["NOTA", "None of the Above"]))
    ]
    return filtered_election_df.shape[0]


def get_form_20_details(year, type,state):
    names_mapping_path = get_name_mappings(year, type, state)

    with open(names_mapping_path, "r") as file:
        names_mapping = json.load(file)

    election_df = get_election_df(type,state)
    # if type == "AE":
    #     election_df = pd.read_csv("data/Chhattisgarh_AE.csv")
    # if type == 'GA':
    #     election_df = pd.read_csv('data/Maharashtra_GA.csv')

    return names_mapping, election_df


def get_candidate_and_form_20_names(form_20_json, election_df, AC, year, top_3=False):
    top_3 = [1, 2, 3]
    if top_3:
        # Define conditions
        condition_general = (
            (election_df["Year"] == year)
            & (election_df["Constituency_No"] == AC)
            & (~election_df["Candidate"].isin(["None of the Above", "NOTA"]))
        )

        condition_inc = election_df["Party"] == "INC"

        # Use bitwise OR to combine conditions
        filtered_election_df = election_df[
            (condition_general & election_df["Position"].isin(top_3))
            | (condition_inc & condition_general)
        ]
    else:
        filtered_election_df = election_df[
            (election_df["Year"] == year)
            & (election_df["Constituency_No"] == AC)
            & (election_df["Candidate"] != "None of the Above")
        ]

    candidates_list = filtered_election_df["Candidate"].tolist()
    form_20_names = [
        i["name"] for i in form_20_json if i["year"] == year and i["AC"] == AC
    ]

    return candidates_list, form_20_names


def fuzzy_match_name_with_tolerance(name, name_list, tolerance=5):
    cleaned_name = name.lower().replace(" ", "").replace(".", "")
    max_score = -1
    matched_name = None
    for candidate_name in name_list:
        cleaned_candidate_name = (
            candidate_name.lower().replace(" ", "").replace(".", "")
        )
        score = fuzz.ratio(cleaned_name, cleaned_candidate_name)
        len_sum = len(cleaned_name) + len(cleaned_candidate_name)
        levenshtein_distance = len_sum - score * len_sum / 100
        if levenshtein_distance <= tolerance:
            if score >= max_score:
                max_score = score
                matched_name = candidate_name

    # If no matches are found, process name parts
    if matched_name is None:
        sub_tolerance = 3
        name = name.replace(".", "")
        name_parts = sorted(
            name.split(), key=len, reverse=True
        )  # Split and sort by length
        filtered_name_parts = [
            part for part in name_parts if len(part) > 2
        ]  # Filter parts greater than 3 characters
        for part in filtered_name_parts:
            part_cleaned = part.lower().replace(" ", "").replace(".", "")
            for candidate_name in name_list:
                cleaned_candidate_name = (
                    candidate_name.lower().replace(" ", "").replace(".", "")
                )

                best_score = 0
                best_distance = float("inf")

                # Sliding window to check every possible substring of candidate name
                for start in range(len(cleaned_candidate_name) - len(part_cleaned) + 1):
                    end = start + len(part_cleaned)
                    candidate_substring = cleaned_candidate_name[start:end]

                    # Calculate fuzzy score and distance for the substring
                    score = fuzz.ratio(part_cleaned, candidate_substring)
                    len_sum = len(part_cleaned) + len(candidate_substring)
                    levenshtein_distance = len_sum - score * len_sum / 100

                    # Update the best score and distance found so far
                    if score > best_score or (
                        score == best_score and levenshtein_distance < best_distance
                    ):
                        best_score = score
                        best_distance = levenshtein_distance

                # If the best score and distance within tolerance, accept it as a match
                if best_distance <= sub_tolerance:
                    matched_name = candidate_name
            if matched_name:
                break

    return matched_name


def get_column_index(column_name, form_20_json, year, AC):
    for i in form_20_json:
        if i["year"] == year and i["AC"] == AC and i["name"] == column_name:
            return i["column"]
    return None


def get_party(election_df, name, year, AC):
    party = election_df[
        (election_df["Year"] == year)
        & (election_df["Constituency_No"] == AC)
        & (election_df["Candidate"] == name)
    ]["Party"].values[0]
    return party



def get_party_mappings(year, AC,state):
    name_mapping, election_df = get_form_20_details(year, AC,state)
    results = []
    candidates_list, form_20_names = get_candidate_and_form_20_names(
        name_mapping, election_df, AC, year, top_3=True
    )

    for candidate in candidates_list:
        matched_name = fuzzy_match_name_with_tolerance(candidate, form_20_names, 5)
        party = get_party(election_df, candidate, year, AC)
        if matched_name:
            column_index = get_column_index(matched_name, name_mapping, year, AC)
            results.append({"column": column_index, "party": party})
    return results


def clean_excel_file(df, year, AC, type,state):
    num_of_candidates = get_columns_details(year,state, type, AC)
    party_mappings = get_party_mappings(year, AC,state)

    # Step 1: Rename Columns based on their expected order and content
    num_cols = df.shape[1]
    number_of_other_columns = num_cols - num_of_candidates - 5
    if number_of_other_columns <= 0:
        raise Exception("Issue in the number of columns in the excel file", year, AC)
    # core_cols = ['SN', 'Polling_Station']
    core_cols = [f"col_{i}" for i in range(1, number_of_other_columns + 1)]

    # Continue with the remaining expected column names
    candidate_cols = [
        f"col_{i}" for i in range(num_cols - num_of_candidates - 4, num_cols - 5 + 1)
    ]

    core_cols += candidate_cols

    nota_check = str(
        df.columns[num_cols - 5]
    ).lower()  # Lowercase the third column name to check properly
    if "none" in nota_check:
        core_cols.append("NOTA")
        core_cols += [
            "Total_Valid_Votes",
            "Total_Rejected_Votes",
            "Total",
            "Total_Votes_Tendered",
        ]
    else:
        core_cols += [
            "Total_Valid_Votes",
            "Total_Rejected_Votes",
            "NOTA",
            "Total",
            "Total_Votes_Tendered",
        ]

    # Apply the new column names
    df.columns = core_cols

    df.rename(columns={"col_1": "SN"}, inplace=True)

    if number_of_other_columns > 1:
        # drop those columns
        df = df.drop(df.columns[1:number_of_other_columns], axis=1)
    # Step 2: Clean all cells in the dataframe to remove unwanted characters
    df = df.applymap(lambda x: "".join(c for c in str(x) if c.isalnum() or c == "."))

    # Step 3: Replace 'nan' strings with actual NaN values
    df.replace(to_replace="^nan$", value=np.nan, regex=True, inplace=True)

    # # Step 4: Convert applicable columns to numeric types
    # # Define columns to exclude from numeric conversion (text columns)
    # exclude_columns = ['SN', 'Polling_Station']

    # Identify columns that should be processed (all except the excluded ones)
    # columns_to_process = df.columns.difference(exclude_columns)

    # Apply numeric conversion only to the appropriate columns
    df = df.apply(pd.to_numeric, errors="coerce")

    # Step 5: Filter out rows where any cell is non-numeric (where it should be numeric)
    df = df[
        df.applymap(lambda x: pd.isna(x) or isinstance(x, (int, float))).all(axis=1)
    ]

    df = df.apply(pd.to_numeric, errors="coerce")

    # Step 1: Identify columns
    col_names = [col for col in df.columns if "col" in col] + ["NOTA"]

    # Step 2: Calculate the sum of the relevant columns
    df["calculated_sum"] = df[col_names].sum(axis=1)

    # Step 3: Calculate the absolute difference between calculated_sum and Total
    df["difference"] = (df["Total"] - df["calculated_sum"]).abs()

    # Step 4: Drop rows where the difference is greater than 50
    df = df[df["difference"] <= 75]

    # Dropping the helper columns as they are no longer needed (optional)
    df.drop(columns=["calculated_sum", "difference"], inplace=True)

    for mapping in party_mappings:
        df = df.rename(columns={f'col_{mapping["column"]}': mapping["party"]})
    df = df[df["SN"].notnull()]

    return df


def clean_and_dump_excel_files(state_name, election_year, constituency_type):
    excel_dir = f"data/Parsed_Excel/{state_name}/{constituency_type}_{election_year}"
    output_dir = f"data/cleaned_excel/{state_name}/{constituency_type}_{election_year}"
    log_file_name = f"logs/clean_{state_name}_{election_year}_{constituency_type}.txt"
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(excel_dir):
        if filename.endswith(".xlsx"):
            try:
                df = pd.read_excel(os.path.join(excel_dir, filename))
                # match = re.search(r'combined_JSON_([a-zA-Z]+)_AssemblyElection_(\d{4})_A(\d{3}).json.xlsx', filename)
                # match = re.search(r'combined_JSON_([a-zA-Z]+)_(\d{4})_AC_(\d{3}).json.xlsx', filename)
                # match = re.search(r'combined_JSON_([a-zA-Z]+)_LokSabha_Election_(\d{4})_AC_(\d{3}).json.xlsx', filename)
                match = re.search(
                    r"combined_JSON_([a-zA-Z]+)_(\d{4})_AC_(\d{3}).json.xlsx", filename
                )

                AC = None
                if match:
                    AC = int(match.group(3))
                cleaned_df = clean_excel_file(df, election_year, AC, constituency_type,state_name)
                cleaned_df["State"] = state_name
                cleaned_df["Year"] = election_year
                cleaned_df["Constituency"] = AC
                output_file_path = os.path.join(output_dir, f"{AC}.xlsx")
                cleaned_df.to_excel(output_file_path, index=False)

            except Exception as exc:
                append_text_to_file(log_file_name,f"Error processing file: {log_file_name} - {exc}\n")
                continue

if __name__ == "__main__":
    # Example usage
    state_name = "MH"
    election_year = "2019"
    # Replace with desired election year
    constituency_type = "AE"  # Replace with desired constituency type (e.g., AE, GE)

    clean_and_dump_excel_files(state_name, election_year, constituency_type)