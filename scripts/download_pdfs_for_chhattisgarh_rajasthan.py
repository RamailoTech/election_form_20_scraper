import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def count_pdf_links(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        pdf_links = []
    
        for link in soup.find_all('a', href=True):
            href = link['href']
            if url == "https://ceorajasthan.nic.in/State_Assembly_Election_2023/Form20_21C_21E.html":
                # Check if href ends with '.pdf'
                if 'Form20' in href and href.endswith('.pdf'):
                    pdf_links.append(href)
            else:
                if href.endswith('.pdf'):
                    pdf_links.append(href)
        
        return pdf_links
    
    return []

def get_election_year(url):
    # Extract election year from the URL (assumes the year is part of the URL)
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    for part in path_parts:
        if part.isdigit() and len(part) == 4:
            return part
    return 'Unknown'

def main(urls, output_folder='PDFs'):
    state_mapping = {
        'https://ceorajasthan.nic.in/Vidhansabha%202018-%20pdf/Form%2020/Form-20.htm': ('Rajasthan', '2018'),
        'https://ceorajasthan.nic.in/State_Assembly_Election_2023/Form20_21C_21E.html': ('Rajasthan', '2023'),
        'https://ceochhattisgarh.nic.in/both/Election23-24_Form_20.html': ('Chhattisgarh', '2023'),
        'https://ceochhattisgarh.nic.in/both/Loksabha_Form_20.html': ('Chhattisgarh', '2018'),  
    }
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for url in urls:
        pdf_links = count_pdf_links(url)
        state_info = state_mapping.get(url, ('Unknown', 'Unknown'))
        state_name, election_year = state_info
        state_folder = os.path.join(output_folder, state_name, election_year)
        
        if not os.path.exists(state_folder):
            os.makedirs(state_folder)
        
        for pdf_link in pdf_links:
            pdf_url = pdf_link
            
            if not pdf_link.startswith('http'):
                pdf_url = url.rsplit('/', 1)[0] + '/' + pdf_link.lstrip('/')
            
            response = requests.get(pdf_url)
            if response.status_code == 200:
                filename = pdf_url.split('/')[-1]
                filepath = os.path.join(state_folder, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"Saved '{filename}' for {state_name} ({election_year}) in {state_folder}")
            else:
                print(f"Failed to download PDF from {pdf_url}")

    print(f"PDFs have been saved to '{output_folder}'.")

if __name__ == '__main__':
    urls = [
        'https://ceorajasthan.nic.in/Vidhansabha%202018-%20pdf/Form%2020/Form-20.htm',
        'https://ceorajasthan.nic.in/State_Assembly_Election_2023/Form20_21C_21E.html',
        'https://ceochhattisgarh.nic.in/both/Election23-24_Form_20.html',
        'https://ceochhattisgarh.nic.in/both/Loksabha_Form_20.html',      
    ]
    
    main(urls)
