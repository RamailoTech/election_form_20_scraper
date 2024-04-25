import os
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from loguru import logger 
import logging

# load_env()

# Configure logging to a file
# logging.basicConfig(filename='logs/Chhattisgarh_AE_2018_filtered_pdfs_parse_logs.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




key='00e66b969a714c0098af538bd68bdb53'
endpoint = 'https://mlexperts-document-intelligence.cognitiveservices.azure.com/'
document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Define the directory path where PDF files are located
# directory_path = "data/PDFs/Chhattisgarh/2018"
document_path = "test_nepali.pdf"


# Specify the folder path to save JSON files
output_folder = "results"

try:
    # Open and process the PDF file
    with open(document_path, "rb") as document:
        poller = document_analysis_client.begin_analyze_document("prebuilt-document", document)
        result = poller.result()
        result_dict = result.to_dict()
        
    # Construct the output file path
    output_filename = f"JSON_test_nepali_2018_{os.path.splitext(document_path)[0]}.json"
    output_file_path = os.path.join(output_folder, output_filename)
    
    # Save the results to a JSON file in the output folder
    with open(output_file_path, "w") as f:
        json.dump(result_dict, f, indent=4)

    print(f"Processed {document_path} and saved results to {output_file_path}")
        
except Exception as e:
    print(f"Failed to process {document_path} due to an error: {e}")

# Create the output folder if it doesn't exist
# os.makedirs(output_folder, exist_ok=True)

# file_name = ['AC08Form20.pdf','AC71Form20.pdf','AC72Form20.pdf']
# # for filename in os.listdir(directory_path):
# for filename in file_name:
#     if filename.endswith(".pdf"):  # Check if the file is a PDF
#         document_path = os.path.join(directory_path, filename)
        
#         try:
#             # Open and process the PDF file
#             with open(document_path, "rb") as document:
#                 poller = document_analysis_client.begin_analyze_document("prebuilt-document", document)
#                 result = poller.result()
#                 result_dict = result.to_dict()
                
#             # Construct the output file path
#             output_filename = f"JSON_chhattisgarh_AssemblyElection_2018_{os.path.splitext(filename)[0]}.json"
#             output_file_path = os.path.join(output_folder, output_filename)
            
#             # Save the results to a JSON file in the output folder
#             with open(output_file_path, "w") as f:
#                 json.dump(result_dict, f, indent=4)

#             print(f"Processed {filename} and saved results to {output_file_path}")
        
#         except Exception as e:
#             logger.error(f"Failed to process {filename} due to an error: {e}")
#             continue  # Skip to the next file
        
#     else:
#         logger.error(f"Skipping {filename}, not a PDF.")
