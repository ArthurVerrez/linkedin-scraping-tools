import argparse
import os
import logging
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from general_lk_utils import (
    remove_url_parameter,
    get_lk_credentials,
    enter_ids_on_lk_signin,
    select_contract_lk,
)

LK_CREDENTIALS_PATH = "./lk_credentials.json"
SCROLL_TO_BOTTOM_COMMAND = "window.scrollTo(0, document.body.scrollHeight);"

RESULT_SELECTOR = "#results-container > span > div > form > ol > li > div > article > div > div > article > div > div.row__card"
IN_RESULT_NAME_SELECTOR = "div.row__top-card > section > div > div.artdeco-entity-lockup__content.lockup__content.ember-view > span > span:nth-child(1) > div > a"
IN_RESULT_ROLE_SELECTOR = "div.row__top-card > section > div > div.artdeco-entity-lockup__content.lockup__content.ember-view > div.artdeco-entity-lockup__subtitle.ember-view"
IN_RESULT_LOCATION_SELECTOR = "div.row__top-card > section > div > div.artdeco-entity-lockup__content.lockup__content.ember-view > div.lockup__details > div > div"
IN_RESULT_INDUSTRY_SELECTOR = "div.row__top-card > section > div > div.artdeco-entity-lockup__content.lockup__content.ember-view > div.lockup__details > div > span:nth-child(2)"
IN_RESULT_EDUCATION_SELECTOR = (
    "div.history > div:nth-child(2) > ol > li > span:nth-child(1)"
)
IN_RESULT_EDUCATION_YEAR_SELECTOR = "div.history > div:nth-child(2) > ol > li > span.row-description-entry__date-duration"
IN_RESULT_SKILL_MATCH = (
    "div.row__card > div:nth-child(3) > dl > div:nth-child(1) > dd > div > button"
)


RESULT_PARSE_INSTRUCTIONS = [
    {
        "name": "name",
        "selector": IN_RESULT_NAME_SELECTOR,
        "depth_in_selector": 0,
        "parse_function": lambda x: x.text.strip(),
    },
    {
        "name": "recruiter_link",
        "selector": IN_RESULT_NAME_SELECTOR,
        "depth_in_selector": 0,
        "parse_function": lambda x: x.get("href"),
    },
    {
        "name": "linkedin_link",
        "selector": IN_RESULT_NAME_SELECTOR,
        "depth_in_selector": 0,
        "parse_function": lambda x: x.get("href").replace("talent/profile", "in"),
    },
    {
        "name": "role",
        "selector": IN_RESULT_ROLE_SELECTOR,
        "depth_in_selector": 0,
        "parse_function": lambda x: x.text.strip(),
    },
    {
        "name": "location",
        "selector": IN_RESULT_LOCATION_SELECTOR,
        "depth_in_selector": 0,
        "parse_function": lambda x: x.text.strip(),
    },
    {
        "name": "industry",
        "selector": IN_RESULT_INDUSTRY_SELECTOR,
        "depth_in_selector": 0,
        "parse_function": lambda x: x.text.strip(),
    },
    {
        "name": "education",
        "selector": IN_RESULT_EDUCATION_SELECTOR,
        "depth_in_selector": 0,
        "parse_function": lambda x: x.text.strip(),
    },
    {
        "name": "education_year",
        "selector": IN_RESULT_EDUCATION_YEAR_SELECTOR,
        "depth_in_selector": 0,
        "parse_function": lambda x: x.text.strip(),
    },
    {
        "name": "skill_match",
        "selector": IN_RESULT_SKILL_MATCH,
        "depth_in_selector": 0,
        "parse_function": lambda x: x.text.strip(),
    },
]

NUMBER_OF_LEADS_PER_PAGE = 25


def get_search_url(search_url_base, start=1):
    url = search_url_base + f"&start={str((start-1)*NUMBER_OF_LEADS_PER_PAGE)}"
    return url


def parse_search_result(result_el, instructions):
    r = {}
    for instruction in instructions:
        r[instruction["name"]] = ""
        els = result_el.select(instruction["selector"])

        if (
            instruction["depth_in_selector"] >= 0
            and len(els) > instruction["depth_in_selector"]
        ):
            r[instruction["name"]] = instruction["parse_function"](
                els[instruction["depth_in_selector"]]
            )

        elif instruction["depth_in_selector"] == -1:
            r[instruction["name"]] = instruction["parse_function"](els)
    return r


def get_search_result_els(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    all_results_el = soup.select(RESULT_SELECTOR)
    return all_results_el


def parse_search_page(page_source):
    all_results_el = get_search_result_els(page_source)
    print(f"Found {len(all_results_el)} results.")
    return [
        parse_search_result(result_el, RESULT_PARSE_INSTRUCTIONS)
        for result_el in all_results_el
    ]


def parse_search_url(url, driver, wait_after_page_loaded=5):
    print(f"Getting and parsing page {url}.")
    driver.get(url)
    time.sleep(wait_after_page_loaded)
    try:
        driver.execute_script(SCROLL_TO_BOTTOM_COMMAND)
    except:
        print("There was an error scrolling down")
    return parse_search_page(driver.page_source)


def scrap_lkr_pages(
    driver,
    page_list,
    get_search_url,
    backups="./backups/",
    wait_time_between_pages=3,
    wait_after_page_loaded=3,
    wait_after_scroll_down=2,
):
    total_info = []
    n_pages = len(page_list)
    for i in range(n_pages):
        p = page_list[i]
        print("-----------")
        print(f"Waiting for {wait_time_between_pages}s...")
        time.sleep(wait_time_between_pages)

        print(f"Getting new page: {p}, ({i+1}/{n_pages}).")
        info = parse_search_url(
            get_search_url(page=p),
            driver,
            wait_after_page_loaded=wait_after_page_loaded,
            wait_after_scroll_down=wait_after_scroll_down,
        )
        total_info += info
        print("-----------")
        if backups:
            df = pd.DataFrame(total_info)
            df.to_csv(
                f"{backups}{str(int(time.time()*1000))}_lk_recruiter_search_export_{i+1}_on_{n_pages}.csv",
                index=False,
            )
    return total_info


if __name__ == "__main__":
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Scrap LinkedIn Recruiter")
    parser.add_argument(
        "--search-url",
        type=str,
        help="The url of the search page to scrap",
        required=True,
    )
    parser.add_argument(
        "--start",
        type=int,
        help="The profile number to start scrapping from",
        required=False,
        default=1,
    )
    parser.add_argument(
        "--end",
        type=int,
        help="The profile number to end scrapping at",
        required=False,
        default=1,
    )
    parser.add_argument(
        "--wait-time-between-pages",
        type=int,
        help="The time in seconds to wait between pages",
        required=False,
        default=5,
    )
    parser.add_argument(
        "--wait-after-page-loaded",
        type=int,
        help="The time in seconds to wait after the page is loaded",
        required=False,
        default=3,
    )
    parser.add_argument(
        "--wait-after-scroll-down",
        type=int,
        help="The time in seconds to wait after scrolling down",
        required=False,
        default=3,
    )
    parser.add_argument(
        "--save-format",
        type=str,
        help="The format to save the data in (xlsx or csv)",
        required=False,
        default="csv",
    )
    args = parser.parse_args()

    # Get the arguments
    search_url = args.search_url
    start = args.start
    end = args.end
    wait_time_between_pages = args.wait_time_between_pages
    wait_after_page_loaded = args.wait_after_page_loaded
    wait_after_scroll_down = args.wait_after_scroll_down
    save_format = args.save_format
    search_url_base = remove_url_parameter(search_url, "start")

    print("Starting the driver...")
    logging.getLogger("selenium").setLevel(logging.CRITICAL)
    # Start the webdriver without any logs
    driver = webdriver.Chrome(options=Options())
    driver.maximize_window()
    driver.get("https://www.linkedin.com/login/")

    print("Inputting the credentials...")
    lk_credentials = get_lk_credentials(LK_CREDENTIALS_PATH)
    enter_ids_on_lk_signin(driver, lk_credentials["email"], lk_credentials["password"])

    if "checkpoint/challenge" in driver.current_url:
        print(
            "It looks like you need to complete a double factor authentification. Please do so and press enter when you are done."
        )
        input()

    print("Selecting the contract...")

    select_contract_lk(driver)

    driver.get(search_url)

    print(
        "Manual actions needed: go to the browser window and unzoom the page so that the whole page fits in the screen in 2 times. Then press enter here."
    )
    input()

    print("Starting the scraping...")

    lkr_search_infos = scrap_lkr_pages(
        driver,
        range(start, end + 1),
        get_search_url=lambda x: get_search_url(search_url_base, start=x),
        backups="./lkr_data/",
        wait_time_between_pages=wait_time_between_pages,
        wait_after_page_loaded=wait_after_page_loaded,
        wait_after_scroll_down=wait_after_scroll_down,
    )

    df = pd.DataFrame(lkr_search_infos)

    if save_format == "csv":
        file_name = f"{str(int(time.time()*1000))}_lk_r_export.csv"
        df.to_csv(f"./lkr_data/{file_name}", index=False)
        print(f"Saved the data in ./lkr_data/{file_name}")
    else:
        # save_format=="xlsx"
        file_name = f"{str(int(time.time()*1000))}_lk_r_export.xlsx"
        df.to_excel(f"./lkr_data/{file_name}", index=False)
        print(f"Saved the data in ./lkr_data/{file_name}")

    print("Done.")
    driver.close()
