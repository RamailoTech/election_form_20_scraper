import json
import os
import re
import sys

# Function to extract mapping entries from a JSON file
def extract_mapping_entries(filename):
    pattern = r"JSON_([A-Z]+)_(\d{4})_([A-Z]+)_(\d{3}).json"
    match = re.search(pattern, filename)
    if match:
        state = match.group(1)
        year = int(match.group(2))
        AC = int(match.group(4))
    else:
        print("Filename donot match the given pattern.")
        return None
    with open(filename) as f:
        data = json.load(f)

    table = data['tables'][0]
    col_headers = []
    cells = table.get('cells')

    for i in range(1,table.get('column_count')):
        col_cells = [cell for cell in cells if cell.get('column_index') == i and cell.get('kind') == 'columnHeader' and cell.get('column_span') == 1]
                
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
        contents = [cell.get('content') for cell in col_cells if not any(term.lower() in (cell.get('content') or "").replace(" ", "").replace("\n","").lower() for term in unwanted_terms)]
  
        contents = [content for content in contents if re.search(r'[a-zA-Z0-9]', content) and len(content) > 4]
        content = contents[0] if len(contents) else None
        if content: 
            col_headers.append({
                "name": content.replace('\n', ' ').strip(),
                "index" : i + 1 
            })

    mapping_entries = []
    for column in col_headers:
        name = column.get('name')
        # name = re.sub(r'[^\x00-\x7F]+', '', name)
        mapping_entry = {
            "state": state,
            "year": year,
            "AC": AC,
            "name": name,
            "column": column.get('index'),
        }
        mapping_entries.append(mapping_entry)

    return mapping_entries



def final_map(state_name, election_year, constituency_type):
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
    final_map(state_name, election_year, constituency_type)

if __name__ == "__main__":
    main()
