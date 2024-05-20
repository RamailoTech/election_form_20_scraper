import os
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()


def append_text_to_file(filename, text):
    """
    Function to append error message to log file.

    Args:
        filename (str): Name of the log file
        text (str): Log message
    """
    if not os.path.exists(filename):
        with open(filename, "a") as file:
            file.write(text + "\n")
    else:
        with open(filename, "a") as file:
            file.write(text + "\n")


# Main function to process PDF files
def process_pdfs(state_name, election_year, constituency_type):
    log_file_name = (
        f"logs/{state_name}_jsonparse_{election_year}_{constituency_type}_log.txt"
    )

    # Load Azure Form Recognizer credentials from environment variables
    key = os.getenv("FORM_RECOGNIZER_KEY")
    endpoint = os.getenv("FORM_RECOGNIZER_ENDPOINT")
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # Define the directory path where PDF files are located
    directory_path = f"data/PDFs/{state_name}/{constituency_type}_{election_year}"

    # Specify the folder path to save JSON files
    output_folder = f"data/Parsed_Pdfs/{state_name}/{constituency_type}_{election_year}"

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):  # Check if the file is a PDF
            document_path = os.path.join(directory_path, filename)

            try:
                # Open and process the PDF file
                with open(document_path, "rb") as document:
                    poller = document_analysis_client.begin_analyze_document(
                        "prebuilt-document", document
                    )
                    result = poller.result()
                    result_dict = result.to_dict()

                # Construct the output file path
                output_filename = f"JSON_{state_name}_{election_year}_{constituency_type}_{os.path.splitext(filename)[0]}.json"
                output_file_path = os.path.join(output_folder, output_filename)

                # Save the results to a JSON file in the output folder
                with open(output_file_path, "w") as f:
                    json.dump(result_dict, f, indent=4)

                print(f"Processed {filename} and saved results to {output_file_path}")

            except Exception as e:
                append_text_to_file(
                    log_file_name, f"Error processing {filename}: {str(e)}\n"
                )
                continue  # Skip to the next file

        else:
            append_text_to_file(log_file_name, f"Skipping {filename}, not a PDF.\n")


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
    process_pdfs(state_name, election_year, constituency_type)

if __name__ == "__main__":
    main()
