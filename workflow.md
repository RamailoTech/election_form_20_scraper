# INC Election Form 20 Scrapper - Knowledge Transfer (KT) Documentation

## Process Overview

### 1. **Download PDFs**
   - **Tools**: Beautiful Soup, `wget`
   - **Task**: Scrape the required sources to download election Form 20 PDFs using Beautiful Soup for web scraping. Use `wget` to download the PDFs from the links extracted by Beautiful Soup.

### 2. **Convert PDF to JSON**
   - **Tools**: Azure PDF conversion service
   - **Task**: Utilize Azure’s PDF conversion service to convert the downloaded PDF files into JSON format for further processing and analysis.

### 3. **Convert JSON to Excel**
   - **Task**: Parse the JSON files and convert them into structured Excel format. This step allows for easier manipulation and analysis of the data.

### 4. **Name Mapping**
   - **Steps**:
     1. Remove irrelevant columns, such as the "Nota" column.
     2. Extract relevant fields from the JSON data for mapping candidate names.
     3. Generate a name mapping JSON file to maintain consistency across candidate names.

### 5. **Data Cleaning**
   - **Task**: Clean the Excel data by:
     - Removing unnecessary characters.
     - Dropping rows with missing or incomplete data.

### 6. **Party Name Mapping Using Fuzzy Matching**
   - **Tools**: CSV file with party names, Fuzzy matching library
   - **Task**: Perform fuzzy matching using a predefined name-mapping file and the provided CSV file with party names and their positions. The goal is to map the top three party names to the corresponding candidates.

### 7. **Create an Intermediate Table**
   - **Task**:
     1. Generate an intermediate table containing:
        - The top three political parties.
        - Their respective vote shares.
        - The total vote count.
     2. Analyze the vote counts to determine whether the Indian National Congress (INC) won or lost in a particular booth.

### 8. **Identify Strong and Swing Booths**
   - **Task**:
     1. Merge intermediate tables for specific years to assess booth performance.
     2. Identify:
        - **Strong booths**: Booths where INC won consistently for around 3 year.
        - **Swing booths**: Booths where INC won at least one year but not consistently across all years.

---

