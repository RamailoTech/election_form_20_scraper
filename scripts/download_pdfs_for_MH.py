import requests
import os

# Base URL structure
base_url = "https://ceoelection.maharashtra.gov.in/form20/LS2019"

# Create a directory to store the downloaded PDFs
output_dir = "data/PDFs/Maharastra/Lok Sabha Election 2019"
os.makedirs(output_dir, exist_ok=True)

# Function to download a single PDF
# Function to download a single PDF
def download_pdf(pc, ac):
    url = f"{base_url}/PC_{str(pc).zfill(2)}/AC_{str(ac).zfill(3)}.pdf"
    response = requests.get(url, verify=False)  # Note the verify=False parameter
    if response.status_code == 200:
        file_path = os.path.join(output_dir, f"PC_{str(pc).zfill(2)}_AC_{str(ac).zfill(3)}.pdf")
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {file_path}")
    else:
        print(f"Not Found: {url}")

# Loop over the range of PC and AC numbers
for pc in range(1, 49):  # PC from 01 to 48
    for ac in range(1, 285):  # AC from 001 to 284
        download_pdf(pc, ac)

print("Download process completed.")



