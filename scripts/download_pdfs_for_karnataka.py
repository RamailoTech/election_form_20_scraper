import requests
import os
from bs4 import BeautifulSoup

# Function to download PDF from a URL
def download_pdf(url, directory):
    filename = os.path.join(directory, url.split("/")[-1])
    with open(filename, 'wb') as f:
        response = requests.get(url)
        f.write(response.content)
        print(f"Downloaded: {filename}")

if __name__ == "__main__":
    base_url = "https://ceo.karnataka.gov.in/form20_2018/PDFS/"
    start_index = 1
    end_index = 224
    directory = "PDFs/Karnataka/Assembly Election 2018"  # Directory to save downloaded PDFs

    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in range(start_index, end_index + 1):
        url = f"{base_url}{i:03d}.pdf"
        download_pdf(url, directory)




#2023

# URL of the page to scrape
url = "https://ceo.karnataka.gov.in/304/_gallery_/en"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find all anchor tags with class 'filelist'
pdf_links = soup.find_all("a", class_="filelist")

# Directory to save the PDFs
save_dir = "data/PDFs/KA/AE 2023"

# Create the directory if it doesn't exist
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Iterate through the links and download PDFs
for link in pdf_links:
    href = link.get("href")
    # Check if the link is a PDF
    if href.endswith(".pdf"):
        pdf_url = href
        # Download the PDF
        pdf_response = requests.get(pdf_url)
        # Extract the filename from the URL
        filename = href.split("/")[-1]
        # Save the PDF to the directory
        with open(os.path.join(save_dir, filename), "wb") as f:
            f.write(pdf_response.content)
            print(f"Downloaded: {filename}")

print("All PDFs downloaded successfully.")









