# LinkedIn Scraping Tools
## Description
This repository is composed of different utilities that can be useful to scrape LinkedIn data. The tools are written in Python and use the Selenium library to interact with the LinkedIn website. The tools are designed to be used with the Chrome web browser, but can be modified to work with other browsers.

Here are the different tools that are currently available:

| Tool | Description | Python file |
| --- | --- | --- |
| LinkedIn Sales Navigator Search Scraper | A tool that scraps the profiles available in a given LinkedIn Sales Nav search | *lksn_search_scraper.py* |
| LinkedIn Sales Navigator Search Visit (WIP) | A tool that takes all the profiles available in a given LinkedIn Sales Nav search and visits their page, providing a visit notification if the privacy settings are correctly set up | *lksn_search_visit.py* |
| LinkedIn Recruiter Search Scraper (WIP) | A tool that scraps the profiles available in a given LinkedIn Recruiter search | *lkr_search_scraper.py* |
| LinkedIn Recruiter Search Visit (WIP) | A tool that takes all the profiles available in a given LinkedIn Recruiter search and visits their page, providing a visit notification if the privacy settings are correctly set up | *lkr_search_visit.py* |

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

--search-url: The URL of the search page to scrape (required).
--start-page: The page to start scraping from (optional, default is 1).
--end-page: The page to end scraping at (optional, default is 1).
--wait-time-between-pages: The time in seconds to wait between pages (optional, default is 5).
--wait-after-page-loaded: The time in seconds to wait after the page is loaded (optional, default is 3).
--wait-after-scroll-down: The time in seconds to wait after scrolling down (optional, default is 3).
--save-format: The format to save the data in (optional, available options: "xlsx" or "csv", default is "csv").

Example
You can run the script with the following command:
```bash	
python lksn_search_scraper.py --search-url "https://www.linkedin.com/sales/search/people?query=(spellCorrectionEnabled%3Atrue%2Ckeywords%3Ascraping)" --start-page 1 --end-page 5 --save-format "csv"
```

### LinkedIn Sales Navigator Search Visit
To come soon...

### LinkedIn Recruiter Search Scraper
To come soon...

### LinkedIn Recruiter Search Scraper
To come soon...

## Disclaimer
The tools and code provided in this repository were created for educational purposes only. Utilizing these tools to scrape or interact with LinkedIn or any other websites in a manner that breaches their terms of service is strictly against the intended use. Anyone who chooses to use these tools in such a way does so at their own risk and assumes all legal responsibility. The author does not endorse or promote any actions that may violate any website's terms of service.

If anyhow you decide to use this tool in a controlled environment, you might get blocked by LinkedIn. The use of LinkedIn Sales Navigator or LinkedIn Recruiter mitigates the limits of the scraping, but it is still possible to get blocked.
