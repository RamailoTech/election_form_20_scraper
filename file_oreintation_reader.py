from PyPDF2 import PdfReader
import os
import pandas as pd

def check_pdf_orientation(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        first_page = reader.pages[0]
        width, height = first_page.mediabox.upper_right
        return height > width  # Return True if the first page is in portrait orientation
    except Exception as e:
        print(f"Unexpected error with {pdf_path}: {e}")
        return None 

def scan_pdfs_for_portrait(folder_path,year,state):
    results = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                full_path = os.path.join(root, filename)
                if check_pdf_orientation(full_path):
                    results.append({
                        'Year': year,
                        'State': state,
                        'Folder Path': root,
                        'Filename': filename
                    })
                

    
    # Saving the results to a CSV file
    results_df = pd.DataFrame(results)
    if not results_df.empty:
        folder_path = "results/Incorrect_orientation"
        csv_path = os.path.join(folder_path, 'RJ_2023.csv')
        results_df.to_csv(csv_path, index=False)
        print(f"CSV file saved: {csv_path}")
    else:
        print("No portrait-oriented PDFs found.")

# Usage of the function
folder_path = 'data/PDFs/Rajasthan/2023'  # Replace with the path to the folder containing your PDFs
scan_pdfs_for_portrait(folder_path,2023,"RJ")




# from PyPDF2 import PdfReader, PdfWriter

# def convert_to_landscape_corrected(pdf_path):
#     reader = PdfReader(pdf_path)
#     writer = PdfWriter()

#     for page in reader.pages:
#         width, height = page.mediabox.upper_right

#         # Check if the page is in portrait mode (height greater than width)
#         if height > width:
#             # Normalize the new rotation to 0-359 degrees
#             new_rotation = (page.rotation + 90) % 360
#             page.rotation = new_rotation
#             print("portrait")
#         else:
#             print("landscape")

#             # # Adjust the page dimensions to match the new rotation
#             # if new_rotation in [90, 270]:
#             #     # Only swap dimensions if in landscape orientation after rotation
#             #     page.mediabox.upper_right = (height, width)
#             #     page.mediabox.lower_left = (0, 0)

#         # Add the adjusted page to the PDF writer
#     #     writer.add_page(page)

#     # # Define the output file path
#     # output_path = 'corrected_output.pdf'
#     # with open(output_path, 'wb') as f:
#     #     writer.write(f)

#     # return output_path

# # Usage of the function
# file_path = 'data/PDFs/Rajasthan/2018/FORM-20_A140.pdf'
# corrected_file_path = convert_to_landscape_corrected(file_path)
# print(f"Corrected PDF saved as: {corrected_file_path}")