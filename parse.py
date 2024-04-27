import os
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from loguru import logger 
import logging

# load_env()

log_file_name = "logs/RJ_jsonparse_2018_AE_rotated_log.txt"
# Configure logging to a file
def append_text_to_file(filename, text):
    # Open the file in append mode ('a') and text mode ('t'), hence 'at'
    with open(filename, 'at') as file:
        # Write the text followed by a newline character
        file.write(text + "\n")


key='00e66b969a714c0098af538bd68bdb53'
endpoint = 'https://mlexperts-document-intelligence.cognitiveservices.azure.com/'
document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Define the directory path where PDF files are located
directory_path = "data/PDFs/Karnataka/KA_2018_Rotated"



# Specify the folder path to save JSON files
output_folder = "results/Parsed_Pdfs/Karnataka/Assembly Election 2018"



# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# file_name = ['AC08Form20.pdf','AC71Form20.pdf','AC72Form20.pdf']
for filename in os.listdir(directory_path):
# for filename in file_name:
    if filename.endswith(".pdf"):  # Check if the file is a PDF
        document_path = os.path.join(directory_path, filename)
        
        try:
            # Open and process the PDF file
            with open(document_path, "rb") as document:
                poller = document_analysis_client.begin_analyze_document("prebuilt-document", document)
                result = poller.result()
                result_dict = result.to_dict()
                
            # Construct the output file path
            output_filename = f"JSON_karnataka_AssemblyElection_2018_{os.path.splitext(filename)[0]}.json"
            output_file_path = os.path.join(output_folder, output_filename)
            
            # Save the results to a JSON file in the output folder
            with open(output_file_path, "w") as f:
                json.dump(result_dict, f, indent=4)

            print(f"Processed {filename} and saved results to {output_file_path}")
        
        except Exception as e:
            append_text_to_file(log_file_name, f"{filename} \n")
            continue  # Skip to the next file
        
    else:
        append_text_to_file(f"Skipping {filename}, not a PDF.")




# import pandas as pd
# from openai import OpenAI

# # Initialize OpenAI client
# client = OpenAI()

# # Function to process names batch-wise
# def process_names_in_batches(names, batch_size=5):
#     for i in range(0, len(names), batch_size):
#         batch = names[i:i+batch_size]
#         # Process batch using OpenAI API
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a language translator. Yor are suppose to translate list of English names into hindi.\n\nTranslate the given names and strictly \nprovide me output in json format.\n\n{'GULAB KAMRO':'hindi name'} "},
#                 {"role": "user", "content": "['GULAB KAMRO', 'CHAMPADEVI PAWLE', 'SHYAM SINGH MARKAM']"},
#             ]
#         )
#         # Handle response from OpenAI API
#         # For example, print completion messages
#         for message in response['choices'][0]['message']['messages']:
#             print(message['content'])

# # Function to read names from CSV file using pandas
# def read_names_from_csv(file_path, column_name):
#     df = pd.read_csv(file_path)
#     names = df[column_name].tolist()
#     return names

# # Example usage
# csv_file_path = 'data.csv'  # Replace 'data.csv' with your CSV file path
# name_column_name = 'name'   # Replace 'name' with the actual column name containing names
# names = read_names_from_csv(csv_file_path, name_column_name)
# process_names_in_batches(names)