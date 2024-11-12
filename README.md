

```markdown
# Web Design and Development Lead Filter

**Web Design and Development Lead Filter** is a Python tool designed to filter leads for web design and development companies by analyzing company websites. Created specifically for lead generation, this program processes lists of companies, examines their websites, and identifies those offering web design or development services based on a predefined set of keywords.

## Features
- Extracts and scans HTML content from company websites
- Identifies keywords related to web design and development to filter relevant companies
- Supports multithreaded processing for faster lead filtering
- Outputs results to CSV, showing which companies were chosen based on criteria

## License
This project is released under the [MIT License](https://opensource.org/licenses/MIT), allowing free usage, modification, and distribution. For commercial use, permission is required. Please contact me at basilbenny1002@gmail.com.

## Input Requirements
- The input file must be a CSV with the following columns:
  - **BusinessName**: Company name
  - **WebsiteURL**: Company website URL

Example `input.csv`:

```csv
BusinessName,WebsiteURL
Example Company,https://example.com
Web Design Co,https://webdesignco.com
Web Development Inc,https://webdevinc.com
```

**Note:** The name of the input and output files can be edited directly in the code.

## Setup and Installation

1. **Clone this repository** to your local machine:
   ```bash
   git clone https://github.com/yourusername/Web-Design-And-Development-Lead-Filter.git
   ```

2. **Navigate to the project folder**:
   ```bash
   cd Web-Design-And-Development-Lead-Filter
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Required libraries include `cloudscraper`, `spaCy`, and others specified in the `requirements.txt`.

4. **Download spaCy language model** (optional, required only for word similarity):
   ```bash
   python -m spacy download en_core_web_sm
   ```
   You can choose from the following spaCy models:
   - **small model**: `en_core_web_sm`
   - **medium model**: `en_core_web_md`
   - **large model**: `en_core_web_lg`

## Running the Program

1. **Prepare your input CSV** file as specified above and place it in the root folder of the project.

2. **Execute the main script**:
   ```bash
   python main.py
   ```

3. **Output**: The program will generate a CSV output containing filtered leads based on keywords:
   - **Company Name**: The name of the business.
   - **Website URL**: URL of the business website.
   - **Keywords**: Identified keywords related to web design or development services.
   - **Chosen**: Yes, No, or Unsure depending on whether the company was flagged as a web design or development lead:
     - **Yes**: Company fits the web design or development criteria.
     - **No**: Company does not meet the criteria.
     - **Unsure**: Unable to determine based on the given criteria.

## How This Project Came to Be
This project was created as a solution to a specific problem I encountered while freelancing for a lead generation company. My task involved analyzing and cleaning up leads to identify companies providing web design and development services. The manual filtering process was inefficient, so I developed this program to automate it.

Now in version 5, this program has evolved through multiple iterations, with improvements made to handle issues like scraping Cloudflare-protected sites. The process taught me a lot about Python, web scraping, and handling large datasets efficiently.

If you have any questions, suggestions, or wish to discuss commercial use, feel free to reach out!
