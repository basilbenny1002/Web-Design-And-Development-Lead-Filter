# Web Design and Development Lead Filter

**Web Design and Development Lead Filter** is a Python tool designed to filter leads for web design and development companies. It helps lead generation teams quickly identify companies offering these services by scanning their websites for relevant keywords. The program processes a list of companies, checks their websites for specific terms, and determines whether they are web design or development-focused.

---

## Features

- Extracts and scans HTML content from company websites.
- Identifies relevant keywords related to web design and development.
- Supports multithreaded processing for faster lead filtering.
- Outputs results to a CSV file, showing whether each company is a lead based on the given criteria.

---

## License

This project is released under the MIT License, allowing free usage, modification, and distribution. Commercial use is allowed, but permission must be sought for such cases. For more information, please contact me at basilbenny1002@gmail.com.

---

## Input Requirements

The input file should be a CSV with the following columns:

- **BusinessName**: The company’s name.
- **WebsiteURL**: The URL of the company’s website.

Example input CSV (`input.csv`):

| BusinessName | WebsiteURL             |
|--------------|------------------------|
| Example Company | https://example.com   |
| Web Design Co | https://webdesignco.com |
| Web Development Inc | https://webdevinc.com |

**Note:** The names of the input and output files can be edited directly in the code.

---

## Setup and Installation

Follow these steps to set up and run the program:

1. **Clone this repository**:
   ```
   git clone https://github.com/basilbenny1002/Web-Design-And-Development-Lead-Filter.git
   ```

2. **Navigate to the project folder**:
   ```
   cd Web-Design-And-Development-Lead-Filter
   ```

3. **Install required dependencies**:
   ```
   pip install -r requirements.txt
   ```
   This will install libraries like `cloudscraper`, `spaCy`, and other necessary packages.

4. **Download the spaCy language model** (only needed if you're using the word similarity feature):
   ```
   python -m spacy download en_core_web_sm
   ```

   You can choose from the following spaCy models:

   - **Small model**: `en_core_web_sm`
   - **Medium model**: `en_core_web_md`
   - **Large model**: `en_core_web_lg`

---

## Running the Program

1. **Prepare your input CSV file** as mentioned above and place it in the root folder of the project.

2. **Run the program**:
   ```
   python main.py
   ```

3. **Output**: The program will generate an output CSV file with the following columns:

   - **Company Name**: The business name.
   - **Website URL**: The URL of the business website.
   - **Keywords**: The relevant keywords found on the website.
   - **Chosen**: A flag indicating whether the company was chosen based on its web design or development services:
     - **Yes**: The company meets the criteria.
     - **No**: The company does not meet the criteria.
     - **Unsure**: The program couldn’t determine based on the keywords.

---

## How This Project Came to Be

I created this project while freelancing for a lead generation company. My role involved cleaning up leads to identify web design and development companies. The process was manual and inefficient, so I developed this program to automate the task and make the process faster and more accurate.

This is now version 5 of the tool, which has improved over time to handle issues like scraping websites protected by Cloudflare. I’ve learned a lot about web scraping, Python, and data processing during this journey.



