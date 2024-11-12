import re
import spacy #Necessary only when finding sublinks based on word similarity
from urllib.parse import urlparse, urlunparse
import pandas as pd
import cloudscraper
from bs4 import BeautifulSoup
import concurrent.futures
import time
import random
from threading import Lock

# Initialize the scraper to mimic a Chrome browser on Windows
scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
    },
)

def remove_trailing_path(url):
    """Removes the trailing path from a URL to get the base URL.
    :param url: str - the full URL to process
    :return: str - the cleaned base URL without the trailing path or parameters"""
    parsed_url = urlparse(url)  # Parse URL into components
    netloc = parsed_url.netloc  # Extract the network location
    path = parsed_url.path.split('/')  # Split the path to handle each component

    if path:
        path.pop()  # Remove the last component of the path

    new_path = '/'.join(part for part in path if part)  # Reconstruct the path
    new_url = urlunparse((netloc, new_path, '', '', '', ''))  # Reconstruct the URL
    final_url = str(new_url).replace(":", "")

    # Ensure HTTPS is included in the final URL output
    if "https://" not in final_url:
        print(f"https://{new_url}")
        return str(f"https://{new_url}")
    else:
        print(f"Good url, {final_url}")
        return final_url

def find_links(text, base_url):
    """Extracts all links within the given HTML text that match a pattern or are relative to base_url.
    :param text: str - HTML text to parse for links
    :param base_url: str - The base URL to resolve relative links
    :return: set - A set of all unique links found"""
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z0-9]|[$\-_.+!*\'(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    links = re.findall(url_pattern, text)
    soup = BeautifulSoup(text, "html.parser")
    a_tags = soup.find_all('a')

    # Attempt to resolve and append relative links
    try:
        for link in a_tags:
            sub_link = link.get('href')
            if base_url in sub_link:
                links.append(sub_link)
            else:
                link.append(f"{base_url}{sub_link}")
    except TypeError as e:
        print(f"Error occurred while finding links for {base_url} using Beautiful soup, type error, nothing to worry about: {e}")
    except Exception as e:
        print(f"Error occurred while trying to find sublinks for {base_url}: {e}")
    return set(links)

class Links():
    """Represents a link and its 'confidence' score based on the link length or similarity for sorting purposes."""
    def __init__(self, link: str, confidence: int):
        self.link = link
        self.confidence = confidence

    # Custom sort based on descending confidence
    def __lt__(self, other):
        return self.confidence > other.confidence
created = 0
class Company():
    """Represents a company and contains methods for looking up keywords on its website."""
    global response, created

    def __init__(self, company_name: str, company_link: str):
        self.name = company_name
        self.link = company_link
        self.keywords =[
    "web design", "website design", "web development", "website development",
    "web and mobile development", "website and mobile development",
    "web applications", "website applications", "wordpress development",
    "web app", "web app design", "website app design", "develop websites",
    "develop custom websites", "web & mobile design", "website & mobile design",
    "web & app development", "website & app development", "ui design",
    "ux design", "ui/ux design", "responsive web design", "responsive website design",
    "ecommerce development", "ecommerce web development", "ecommerce website design",
    "frontend web development", "frontend website development", "backend web development",
    "backend website development", "digital design", "website maintenance",
    "web maintenance", "website redesign", "web redesign", "custom websites",
    "custom web design", "custom website design", "web solutions", "website solutions",
    "web consultancy", "website consultancy", "seo optimization", "seo services",
    "content management systems", "cms development", "cms solutions",
    "mobile-friendly websites", "website optimization", "web optimization",
    "interactive web design", "interactive website design", "landing page design",
    "web application development", "website application development",
    "custom website development", "design and development", "web and software development",
    "website and software development", "web-based application", "website-based application",
    "web site design", "website needs", "web & mobile", "website & mobile",
    "web & graphic design", "website & graphic design", "website consulting",
    "web consulting", "build beautiful websites", "customized websites",
    "web design solutions", "website design solutions", "creative web design",
    "creative website design", "digital branding", "web branding", "website branding",
    "web and app solutions", "website and app solutions", "website application design",
    "web user interface", "website user interface", "interactive design",
    "web design and app development", "website design and app development",
    "web development and app development", "website development and app development",
    "web design and mobile app development", "website design and mobile app development",
    "web development and mobile app development", "website development and mobile app development",
    "web design and development", "web development and design",
    "website design & development", "website development & design",
    "web design + development", "web development + design",
    "web design & development services", "website design & development services",
    "web design and development company", "website design and development company", "web & app development"
]
        self.increment()
    def increment(self):
        global created
        created += 1
    def Look_for_keywords(self):
        """Attempts to retrieve website content and search for specified keywords.
        :return: list - Contains company name, URL, found keywords, and a status code"""
        try:
            link = remove_trailing_path(self.link)
        except Exception as e:
            # Handle invalid or broken link cases
            if len(self.link) < 3:
                return [self.name, "Invalid link", "No keywords", "0"]
            else:
                return [self.name, f"Some error occurred: {e}", "No keywords", "3"]
        else:
            try:
                response = scraper.get(link)  # Attempt to fetch website content
            except Exception as e:
                return [self.name, self.link, f"Exception occurred: {e}", "3"]

        # Check if the website response was successful
        if str(response.status_code) == '200':
            data = response.text.lower()
            found_keywords = [keyword for keyword in self.keywords if keyword in data]

            # Return found keywords or continue to look for related sub-links if none are found
            if found_keywords:
                return [self.name, self.link, " ".join(found_keywords), "1"]
            else:
                return self._look_for_sub_links(data)
        elif str(response.status_code) == '404':
            return [self.name, self.link, "Website not found", "0"]
        else:
            return [self.name, self.link, f"Need human support, {response}", "3"]

    def _look_for_sub_links(self, response: str):
        """Searches sub-links of the site if keywords are not directly found.
        :param response: str - HTML content of the main page
        :return: list - Contains company name, URL, found keywords, and a status code"""
        print(f"Looking for sub-links for {self.link}")
        found_urls = find_links(response, base_url=self.link)
        try:
            links = [Links(url, len(url)) for url in found_urls if self.link in url and url.count('/') < 7]
        except:
            return [self.name, self.link, "No keywords found", "0"]
        # TODO: Uncomment the following section to use spaCy for similarity matching with certain keywords, make sure to comment the above line while using spacy
        # nlp = spacy.load("en_core_web_md")
        #similarity = 0.45 # Adjust threshold as needed
        # target_keywords = ["services", "capabilities", "solutions", "expertise", "offerings"]
        # level_one = []
        # for i in target_keywords:
        #     string = f"{self.link}{i}"  ##Combines the website link with the keyword
        #     level_one.append(string)
        # modified_keywords = [''.join(e for e in level_one if e.isalpha())]                  ##Removes symbols from the string, since most Spacy models can't process symbols
        # link_dict = {''.join(e for e in link if e.isalpha()):link for link in found_urls}        ##Makes a dictionary with the actual link and the modified link
        ##The following for loop looks for similarity with the target keywords
        # for link in link_dict:
        #     link_doc = nlp(link.lower())
        #     max_similarity = max(link_doc.similarity(nlp(keyword)) for keyword in modified_keywords)
        #     if max_similarity > similarity:
        #         service_link.append(Links(link, int(max_similarity)))
        # links
        #
        # = sorted(service_link) #Sort the link based on similarity
        # TODO: Spacy part ends

        for l in sorted(links):
            time.sleep(random.randint(1, 4))  # Rate limit requests to avoid blocking
            resp = scraper.get(l.link)
            if str(resp.status_code) == '200':
                data = resp.text.lower()
                found_keywords = [keyword for keyword in self.keywords if keyword in data]
                if found_keywords:
                    return [self.name, self.link, " ".join(found_keywords), "1"]

        return [self.name, self.link, "No keywords found", "0"]
process_company_called = 0
def process_company(i, companies, links):
    global process_company_called
    """Processes individual companies to search for keywords.
    :param i: int - Index of the company
    :param companies: list - List of company names
    :param links: list - List of company URLs"""
    process_company_called += 1
    time.sleep(random.randint(1, 4))  # Random delay to avoid rate-limiting issues
    try:
        if len(str(links[i])) > 4:
            c = Company(companies[i], links[i])
            result = c.Look_for_keywords()
        else:
            result = [companies[i], links[i], "No keywords, invalid link", "0"]

        # Use lock to append results safely in a multithreaded context
        with Lock():
            output.append(result)
    except Exception as e:
        print(f"Exception happened{e}")

def main(companies, links):
    """Executes the keyword search in a multithreaded environment.
    :param companies: list - List of company names
    :param links: list - List of URLs for each company"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_company, i, companies, links) for i in range(len(companies))]
        concurrent.futures.wait(futures)

# Load companies and URLs from CSV file
input_file = "Fullfilledge USA - Fort Wayne, IN(Finished)proper one.csv" #replace with input file path (Must be a CSV)
output_file = "output.csv" #replace with output file path
df = pd.read_csv(input_file)
companies = df['BusinessName'].tolist()
links = df['WebsiteURL'].tolist()

# Run the main function and handle the output
output = [] #List to collect all the rows of teh output file
try:
    main(companies=companies, links=links)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    output_file = pd.DataFrame(output, columns=["Company Name", "WebsiteUrl", "Keywords", "Chosen"])
    output_file.to_csv(path_or_buf=output_file, index=False)
    print(f"Finished going through a list of {len(companies)}, found valid websites for {created} and finished cleaning")
