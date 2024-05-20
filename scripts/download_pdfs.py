import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys

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

def count_pdf_links(url, state_name, election_year):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        pdf_links = []
    
        for link in soup.find_all('a', href=True):
            href = link['href']
            if state_name == 'Rajasthan' and election_year == '2023':
                # Check if href ends with '.pdf' and contains 'Form20'
                if 'Form20' in href and href.endswith('.pdf'):
                    pdf_links.append(href)
            else:
                if href.endswith('.pdf'):
                    pdf_links.append(href)
        
        return pdf_links
    
    return []

def download_pdf(url, directory):
    filename = os.path.join(directory, url.split("/")[-1])
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        append_text_to_file(log_filename, f"Failed to download PDF from {url}")

def download_maharashtra_pdfs(base_url, output_dir):
    for pc in range(1, 49):  # PC from 01 to 48
        for ac in range(1, 285):  # AC from 001 to 284
            url = f"{base_url}/PC_{str(pc).zfill(2)}/AC_{str(ac).zfill(3)}.pdf"
            response = requests.get(url, verify=False)  # Note the verify=False parameter
            if response.status_code == 200:
                file_path = os.path.join(output_dir, f"PC_{str(pc).zfill(2)}_AC_{str(ac).zfill(3)}.pdf")
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                append_text_to_file(log_filename, f"Not Found: {url}")

def main(state_name, election_year, constituency_type):
    output_folder = 'data/PDFs'
    global log_filename
    log_filename = f'logs/download_pdfs_{state_name}_{election_year}_{constituency_type}.txt'
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    base_urls = {
        'RJ': {
            'AE_2018': 'https://ceorajasthan.nic.in/Vidhansabha%202018-%20pdf/Form%2020/Form-20.htm',
            'AE_2023': 'https://ceorajasthan.nic.in/State_Assembly_Election_2023/Form20_21C_21E.html'
        },
        'CH': {
            'AE_2018': 'https://ceochhattisgarh.nic.in/both/Loksabha_Form_20.html',
            'AE_2023': 'https://ceochhattisgarh.nic.in/both/Election23-24_Form_20.html'
        },
        'KA': {
            'AE_2018': 'https://ceo.karnataka.gov.in/form20_2018/PDFS/',
            'AE_2023': 'https://ceo.karnataka.gov.in/304/_gallery_/en'
        },
        'MH': {
            'GA_2019': 'https://ceoelection.maharashtra.gov.in/form20/LS2019'
        }
    }

    url_key = f"{constituency_type}_{election_year}"
    url = base_urls.get(state_name, {}).get(url_key, None)
    if not url:
        print(f"No URL found for state '{state_name}', year '{election_year}', and constituency type '{constituency_type}'.")
        return
    
    state_folder = os.path.join(output_folder, state_name, f'{constituency_type} {election_year}')

    if not os.path.exists(state_folder):
        os.makedirs(state_folder)

    if state_name == 'KA' and election_year == '2018':
        base_url = url
        start_index = 1
        end_index = 224

        for i in range(start_index, end_index + 1):
            pdf_url = f"{base_url}{i:03d}.pdf"
            download_pdf(pdf_url, state_folder)

    elif state_name == 'KA' and election_year == '2023':
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            pdf_links = soup.find_all("a", class_="filelist")
            
            for link in pdf_links:
                href = link.get("href")
                if href.endswith(".pdf"):
                    pdf_url = urljoin(url, href)
                    download_pdf(pdf_url, state_folder)
        else:
            append_text_to_file(log_filename, f"Failed to scrape the URL: {url}")

    elif state_name == 'MH' and election_year == '2019':
        download_maharashtra_pdfs(url, state_folder)
        

    else:
        pdf_links = count_pdf_links(url, state_name, election_year)
        
        for pdf_link in pdf_links:
            pdf_url = urljoin(url, pdf_link)  # Ensure correct URL joining
            download_pdf(pdf_url, state_folder)

    print(f"PDFs have been saved to '{state_folder}'.")

def final_main():
    # Check if the required arguments are provided
    if len(sys.argv) < 4:
        print("Usage: python json_to_excel.py <state_name> <election_year> <constituency_type>")
        sys.exit(1)

    # Get the arguments from the command line
    state_name = sys.argv[1]
    election_year = sys.argv[2]
    constituency_type = sys.argv[3]

    # Call the function to process the JSON files
    main(state_name, election_year, constituency_type)

if __name__ == "__main__":
    final_main()

