import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def append_text_to_file(filename, text):
    """
    Function to append error message to log file.

    Args:
        filename (str): Name of the log file
        text (str): Log message
    """
    with open(filename, 'a') as file:
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

def main(state_name, election_year):
    output_folder = 'data/PDFs'
    global log_filename
    log_filename = f'logs/download_pdfs_{state_name}_{election_year}.txt'
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    base_urls = {
        'RJ': {
            '2018': 'https://ceorajasthan.nic.in/Vidhansabha%202018-%20pdf/Form%2020/Form-20.htm',
            '2023': 'https://ceorajasthan.nic.in/State_Assembly_Election_2023/Form20_21C_21E.html'
        },
        'CH': {
            '2018': 'https://ceochhattisgarh.nic.in/both/Loksabha_Form_20.html',
            '2023': 'https://ceochhattisgarh.nic.in/both/Election23-24_Form_20.html'
        },
        'KA': {
            '2018': 'https://ceo.karnataka.gov.in/form20_2018/PDFS/',
            '2023': 'https://ceo.karnataka.gov.in/304/_gallery_/en'
        },
        'MH': {
            '2019': 'https://ceoelection.maharashtra.gov.in/form20/LS2019'
        }
    }

    url = base_urls.get(state_name, {}).get(election_year, None)
    if not url:
        print(f"No URL found for state '{state_name}' and year '{election_year}'.")
        return
    
    if state_name == 'KA' and election_year == '2018':
        base_url = url
        start_index = 1
        end_index = 224
        state_folder = os.path.join(output_folder, 'Karnataka', 'Assembly Election 2018')

        if not os.path.exists(state_folder):
            os.makedirs(state_folder)

        for i in range(start_index, end_index + 1):
            pdf_url = f"{base_url}{i:03d}.pdf"
            download_pdf(pdf_url, state_folder)

    elif state_name == 'KA' and election_year == '2023':
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            pdf_links = soup.find_all("a", class_="filelist")
            state_folder = os.path.join(output_folder, 'Karnataka', 'Assembly Election 2023')
            
            if not os.path.exists(state_folder):
                os.makedirs(state_folder)
            
            for link in pdf_links:
                href = link.get("href")
                if href.endswith(".pdf"):
                    pdf_url = urljoin(url, href)
                    download_pdf(pdf_url, state_folder)
        else:
            append_text_to_file(log_filename, f"Failed to scrape the URL: {url}")

    elif state_name == 'MH' and election_year == '2019':
        state_folder = os.path.join(output_folder, 'Maharashtra', 'Lok Sabha Election 2019')
        if not os.path.exists(state_folder):
            os.makedirs(state_folder)
        download_maharashtra_pdfs(url, state_folder)

    else:
        pdf_links = count_pdf_links(url, state_name, election_year)
        
        state_folder = os.path.join(output_folder, state_name, election_year)
        if not os.path.exists(state_folder):
            os.makedirs(state_folder)
        
        for pdf_link in pdf_links:
            pdf_url = urljoin(url, pdf_link)  # Ensure correct URL joining
            download_pdf(pdf_url, state_folder)

    print(f"PDFs have been saved to '{output_folder}'.")

if __name__ == '__main__':
    # Example usage
    state_name = 'RJ'
    election_year = '2023'
    
    main(state_name, election_year)
