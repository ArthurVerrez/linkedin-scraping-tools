# LinkedIn Scraping Tools with Selenium
## Description
This repository is composed of different utilities that can be useful to scrape LinkedIn data. The tools are written in Python and use the Selenium library to interact with the LinkedIn website. The tools are designed to be used with the Chrome web browser, but can be modified to work with other browsers.

Here are the different tools that are currently available:

| Tool | Description | Python file | LinkedIn Plan Compatibility |
| --- | --- | --- | --- |
| LinkedIn Sales Navigator Search Scraper | A tool that scraps the profiles available in a given LinkedIn Sales Nav search | *lksn_search_scraper.py* | Any Sales Navigator |
| LinkedIn Recruiter Search Scraper | A tool that scraps the profiles available in a given LinkedIn Recruiter search | *lkr_search_scraper.py* | Recruiter, Recruiter Lite |
| LinkedIn Visitor | A tool that takes all the profiles available in a given LinkedIn Recruiter search and visits their page, providing a visit notification if the privacy settings are correctly set up | *lk_visitor.py* | Any (even free, but careful of the limitations) |

## Installation
```bash
git clone https://github.com/ArthurVerrez/linkedin-scraping-tools.git
cd linkedin-scraping-tools
pip install -r requirements.txt
```

Create a new file called *lk_credentials.json* at the root of the project and add the following content:
```json
{
    "email": "YOUR_LINKEDIN_EMAIL",
    "password": "YOUR_LINKEDIN_PASSWORD"
}
```

## Usage
### LinkedIn Sales Navigator Search Scraper
Below are the options you can use:

*--search-url*: The URL of the search page to scrape (required).\
*--start-page*: The page to start scraping from (optional, default is 1).\
*--end-page*: The page to end scraping at (optional, default is 1).\
*--wait-time-between-pages*: The time in seconds to wait between pages (optional, default is 5).\
*--wait-after-page-loaded*: The time in seconds to wait after the page is loaded (optional, default is 3).\
*--wait-after-scroll-down*: The time in seconds to wait after scrolling down (optional, default is 3).\
*--save-format*: The format to save the data in (optional, available options: "xlsx" or "csv", default is "csv").

#### Example
You can run the script with the following command:
```bash	
python lksn_search_scraper.py --search-url "https://www.linkedin.com/sales/search/people?query=(spellCorrectionEnabled%3Atrue%2Ckeywords%3Ascraping)" --start-page 1 --end-page 5 --save-format "csv"
```

### LinkedIn Recruiter Search Scraper
Below are the options you can use:

*--search-url*: The URL of the search page to scrape (required).\
*--start*: The profile number to start scraping from (optional, default is 1).\
*--end*: The profile number to end scraping at (optional, default is 1).\
*--wait-time-between-pages*: The time in seconds to wait between pages (optional, default is 5).\
*--wait-after-page-loaded*: The time in seconds to wait after the page is loaded (optional, default is 3).\
*--wait-after-scroll-down*: The time in seconds to wait after scrolling down (optional, default is 3).\
*--save-format*: The format to save the data in (optional, available options: "xlsx" or "csv", default is "csv").

#### Example
You can run the script with the following command:
```bash
python lkr_search_scraper.py --search-url "https://www.linkedin.com/talent/search?searchContextId=8fe5d263-7739-471f-89ea-6b0a4d0fd91d&searchHistoryId=5262292356&searchRequestId=ca1839e7-ba16-4ad4-80ed-d13873939073" --start 5 --end 20 --save-format "csv"
```

### LinkedIn Visitor
Below are the options you can use:

*--profile_file*: Path to the file containing the profiles to visit (accepts .csv and .xlsx as long as it has a column named 'linkedin_url') (required).\
*--shortest_wait_time*: Shortest wait time in seconds between actions (optional, default is 4).\
*--longest_wait_time*: Longest wait time in seconds between actions (optional, default is 7).\
*--page_load_time*: Time to wait in seconds for the page to load (optional, default is 3).

#### Example
You can run the script with the following command:
```bash
python your_script_name.py --profile_file "./lksn_data/1692694694168_lk_salesnav_export.csv" --shortest_wait_time 3 --longest_wait_time 8 --page_load_time 4
```



## Disclaimer
The tools and code provided in this repository were created for educational purposes only. Utilizing these tools to scrape or interact with LinkedIn or any other websites in a manner that breaches their terms of service is strictly against the intended use. Anyone who chooses to use these tools in such a way does so at their own risk and assumes all legal responsibility. The author does not endorse or promote any actions that may violate any website's terms of service.

If anyhow you decide to use this tool in a controlled environment, you might get blocked by LinkedIn. The use of LinkedIn Sales Navigator or LinkedIn Recruiter mitigates the limits of the scraping, but it is still possible to get blocked.
