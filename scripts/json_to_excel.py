import json
import pandas as pd
import os
from collections import defaultdict
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


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


def check_column_lengths(df_list):
    """Function to check column lengths of DataFrames"""
    column_lengths = [set(df.columns) for df in df_list]
    return column_lengths


def concatenate_dfs(df_list):
    """Function to concatenate DataFrames"""
    grouped_dfs = defaultdict(list)
    for df in df_list:
        grouped_dfs[len(df.columns)].append(df)

    merged_dfs = []
    for key in grouped_dfs:
        standard_columns = grouped_dfs[key][0].columns
        adjusted_dfs = []

        for df in grouped_dfs[key]:
            df_new = df.copy()
            df_new.columns = standard_columns
            adjusted_dfs.append(df_new)

        merged_df = pd.concat(adjusted_dfs, ignore_index=True)
        merged_dfs.append(merged_df)

    return merged_dfs


def get_column_headers(table, col_count, table_index):
    """Function to get column headers from table"""
    col_headers = []
    cells = table.get("cells")
    if table_index == 0:
        for i in range(col_count):
            col_cells = [
                cell
                for cell in cells
                if cell.get("column_index") == i and cell.get("kind") == "columnHeader"
            ]
            if col_cells:
                max_row_in_column = max([cell.get("row_index") for cell in col_cells])
                for cell in col_cells:
                    if cell.get("row_index") == max_row_in_column:
                        header_content = cell.get("content")
                        col_headers.append(
                            header_content if header_content else f"Unnamed: {i}"
                        )
            else:
                col_headers.append(f"Unnamed: {i}")
    else:
        for i in range(col_count):
            col_headers.append(f"Unnamed: {i}")
    return col_headers


def get_table_data(table):
    """Function to get table data from table"""
    table_data = []
    cells = table.get("cells")
    for row in range(table.get("row_count")):
        row_content = []
        for col in range(table.get("column_count")):
            cell = next(
                (
                    cell
                    for cell in cells
                    if cell.get("row_index") == row and cell.get("column_index") == col
                ),
                None,
            )
            row_content.append(
                cell.get("content") if cell and cell.get("kind") == "content" else None
            )
        if not all(value is None for value in row_content):
            table_data.append(row_content)
    return table_data


def clean_df(df):
    """Function to clean DataFrame"""
    df.replace(
        to_replace=r":unselected:|:selected:", value="", regex=True, inplace=True
    )

    def clean_cell(x):
        if isinstance(x, str):
            parts = x.strip().split()
            last_part = parts[-1] if parts else ""
            return re.sub(r"[^a-zA-Z0-9]", "", last_part)
        return x

    cleaned_df = df.applymap(clean_cell)
    return cleaned_df


def process_json_files(state_name, election_year, constituency_type):
    """Main function to process JSON files"""
    input_dir = f"data/Parsed_Pdfs/{state_name}/{constituency_type}_{election_year}"
    output_dir = f"data/Parsed_Excel/{state_name}/{constituency_type}_{election_year}"
    log_file_name = (
        f"logs/{state_name}_json_to_excel_{constituency_type}_{election_year}.txt"
    )

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            with open(os.path.join(input_dir, filename)) as f:
                data = json.load(f)
            try:
                tables = data["tables"]
                tables_df = []
                for table_index, table in enumerate(tables):
                    table_data = get_table_data(table)
                    initial_df = pd.DataFrame(table_data)
                    current_headers = get_column_headers(
                        table, col_count=initial_df.shape[1], table_index=table_index
                    )
                    df = pd.DataFrame(table_data, columns=current_headers)
                    tables_df.append(df)

                if tables_df:
                    merged_dfs = concatenate_dfs(tables_df)
                else:
                    print(f"No tables found in {filename}")
                    continue

                output_file = os.path.join(
                    output_dir, f"combined_{os.path.splitext(filename)[0]}.xlsx"
                )
                with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
                    for index, df in enumerate(merged_dfs):
                        sheet_name = f"Sheet_{index+1}"
                        cleaned_df = clean_df(df)
                        cleaned_df.to_excel(writer, index=False, sheet_name=sheet_name)

                print(f"Processed {filename} and saved results to {output_file}")

            except Exception as exc:
                append_text_to_file(
                    log_file_name, f"Error processing {filename}: {str(exc)}\n"
                )


if __name__ == "__main__":
    # Example usage
    state_name = "CH"
    election_year = "2023"  # Replace with desired election year
    constituency_type = "AE"  # Replace with desired constituency type (e.g., AE, GE)

    process_json_files(state_name, election_year, constituency_type)
