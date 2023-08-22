import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import json
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

SELECT_CONTRACT_BUTTON_SELECTOR = "#main > div > div > div:nth-child(3) > form > div > ul > li:nth-child(1) > div > div.contract-list__item-buttons > button"


def get_lk_credentials(path="./lk_credentials.json"):
    f = open(path)
    data = json.load(f)
    f.close()
    return data


def enter_ids_on_lk_signin(driver, email, password):
    time.sleep(2)
    usernameInputElement = driver.find_element(By.ID, "username")
    usernameInputElement.send_keys(email)
    passwordInputElement = driver.find_element(By.ID, "password")
    passwordInputElement.send_keys(password)
    submitElement = driver.find_element(
        By.CSS_SELECTOR,
        "#organic-div > form > div.login__form_action_container > button",
    )
    time.sleep(1)
    submitElement.click()
    time.sleep(5)


def get_lk_url_from_sales_lk_url(url):
    parsed = re.search("/lead/(.*?),", url, re.IGNORECASE)
    if parsed:
        return f"https://www.linkedin.com/in/{parsed.group(1)}"
    return None


def select_contract_lk(driver):
    contract_filter = driver.find_element(
        By.CSS_SELECTOR, SELECT_CONTRACT_BUTTON_SELECTOR
    )
    contract_filter.click()
    time.sleep(4)
    return


def remove_url_parameter(url, param):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if param in query_params:
        del query_params[param]

    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query,
            parsed_url.fragment,
        )
    )

    return new_url
