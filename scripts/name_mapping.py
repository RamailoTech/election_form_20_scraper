import json
import os
import re


# Function to extract mapping entries from a JSON file
def extract_mapping_entries(filename):
    match = re.search(r"JSON_([a-zA-Z]+)_(\d{4})_AC_(\d{2}).json", filename)
    # match = re.search(r'JSON_([a-zA-Z]+)_(\d{4})_AC_(AC\d{2})Form\d{2}\.json',filename)
    # match = re.search(r'JSON_([a-zA-Z]+)_LokSabha_Election_(\d{4})_AC_(\d{3}).json', filename)

    # match = re.search(r"Form20-(\d+)", filename)
    # match = re.search(r'JSON_([a-zA-Z]+)_(\d{4})_AC_(AC\d{2})Form\d{2}\.json',filename)

    if match:
        # state = match.group(1).lower()  # Convert state name to lowercase
        # state = match.group(1).lower()
        state = "CH"
        year = int(match.group(2))
        AC = int(match.group(3))
    else:
        print(f"Filename {filename} does not match expected format.")
        return []

    with open(filename) as f:
        data = json.load(f)

    table = data["tables"][0]
    col_headers = []
    cells = table.get("cells")

    for i in range(1, table.get("column_count")):
        col_cells = [
            cell
            for cell in cells
            if cell.get("column_index") == i
            and cell.get("kind") == "columnHeader"
            and cell.get("column_span") == 1
        ]

        # contents = [cell.get('content') for cell in col_cells]
        
        if state == "CH":
            unwanted_terms = [
                "मतदान",
                "केन्द्र",
                "क्रम",
                "संख्या",
                "विधिमान्य",
                "मतों",
                "नोटा",
                "एनओटीए",
                "निविदत्त",
                "कुल",
                "NOTA",
                "अस्वीकृत",
                "स.क.",
                "इनमें",
                "कोई",
                "नही",
                "पार्टी",
                "बहुजन",
                "मुक्ति",
                "समाज",
                "इंडियन",
                "नेशनल",
                "कौंग्रेस",
                "छत्तीसगढ़",
                "स्वाभिमान",
                "मंच",
                "आबडकराइट",
                "ऑफ",
                "आम",
                "आदमी",
                "निर्दलीय",
                "बहुजन",
                "(भा.ज.पा.)",
                "(ब.स.पा.)",
                "(इं.ने.कां.)",
                "(आ.आ.पा.)",
                "(जद यू.)",
                "(निर्दलीय)",
                "विकल्प",
            ]
        unwanted_terms = [
            "NOTA",
            "None",
            "station",
            "polling",
            "total",
            "vote",
            "rendered",
            "rejected",
            "valid",
            "serial",
        ]

        # Filtering out the cells whose content contains any of the unwanted terms
        contents = [
            cell.get("content")
            for cell in col_cells
            if not any(
                term.lower()
                in (cell.get("content") or "")
                .replace(" ", "")
                .replace("\n", "")
                .lower()
                for term in unwanted_terms
            )
        ]

        contents = [
            content
            for content in contents
            if re.search(r"[a-zA-Z0-9]", content) and len(content) > 4
        ]
        content = contents[0] if len(contents) else None
        if content:
            col_headers.append(
                {"name": content.replace("\n", " ").strip(), "index": i + 1}
            )

    mapping_entries = []
    for column in col_headers:
        name = column.get("name")
        name = re.sub(r"[^\x00-\x7F]+", "", name)
        mapping_entry = {
            "state": state,
            "year": year,
            "AC": AC,
            "name": name,
            "column": column.get("index"),
        }
        mapping_entries.append(mapping_entry)

    return mapping_entries


def main(state_name, election_year, constituency_type):
    # folder_path = 'results/Parsed_Pdfs/RA_filtered/2023'

    folder_path = f"data/Parsed_Pdfs/{state_name}/{constituency_type}_{election_year}"
    # folder_path = 'results/Parsed_Pdfs/Maharastra/Lok Sabha Election 2019'
    final_mapping_entries = []

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            mapping_entries = extract_mapping_entries(file_path)
            final_mapping_entries.extend(mapping_entries)

    # Write final mapping entries to a JSON file
    final_mapping_filename = (
        f"data/name_mappings/{state_name}_{election_year}_{constituency_type}.json"
    )

    with open(final_mapping_filename, "w") as f:
        json.dump(final_mapping_entries, f, indent=4)

    print(f"Final mapping file created: {final_mapping_filename}")


if __name__ == "__main__":
    # Example usage
    state_name = "CH"
    election_year = "2023"  # Replace with desired election year
    constituency_type = "AE"  # Replace with desired constituency type (e.g., AE, GE)

    main(state_name, election_year, constituency_type)
