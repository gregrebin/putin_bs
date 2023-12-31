import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from fp.fp import FreeProxy

FILENAME = "links8.txt"
USER_AGENT = "-u" in sys.argv
HEADLESS = "-h" in sys.argv
PROXY = "-p" in sys.argv
CUSTOM_PROXY = list(filter(lambda arg: arg.startswith("-p="), sys.argv))


def get_links(filename):
    file = open(filename, "r")
    links = file.readlines()
    file.close()
    return links


def setup_driver():
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    if CUSTOM_PROXY:
        proxy = CUSTOM_PROXY[0].removeprefix("-p=")
        options.add_argument(f"--proxy-server={proxy}")
        print(f"Connecting to proxy {proxy}")
    elif PROXY:
        proxy = FreeProxy(google=True, rand=True).get()
        options.add_argument(f"--proxy-server={proxy}")
        print(f"Connecting to proxy {proxy}")
    if USER_AGENT:
        user_agent = UserAgent().random
        options.add_argument(f"--user-agent={user_agent}")
        print(f"With user agent {user_agent}")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    return driver


def download_text(driver, link):
    driver.get(link)
    text = driver.find_element(By.CLASS_NAME, "read__content").text
    date = driver.find_element(By.CLASS_NAME, "read__published").get_attribute("datetime")
    with open(f"content/{date}.txt", "a") as file:
        file.write(text)


def write_remaining(filename, links):
    with open(filename, "w") as file:
        for remaining in links:
            file.write(remaining)


def main(filename):
    links = get_links(filename)
    driver = setup_driver()
    i = 1
    total = len(links)
    for link in links[:]:
        try:
            print(link)
            print(f"{str(i)}/{str(total)}")
            download_text(driver, link)
            links.remove(link)
            time.sleep(1)
            i += 1
        except (Exception, KeyboardInterrupt):
            write_remaining(filename, links)
            return
    os.remove(filename)


if __name__ == '__main__':
    main(FILENAME)

