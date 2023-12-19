import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import re

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver = webdriver.Chrome()
    links = set()
    for i in range(1, 491):
        url = "http://en.kremlin.ru/events/president/transcripts/page/" + str(i)
        print(url)
        driver.get(url)
        elements = driver.find_elements(By.TAG_NAME, "a")
        for element in elements:
            href = element.get_attribute("href")
            if href is None:
                continue
            match = re.search("^http://en.kremlin.ru/events/president/transcripts/\d{5}$", href)
            if match is None:
                continue
            links.add(href)
        time.sleep(3)
    file = open("links.txt", "a")
    for link in links:
        file.write(link + "\n")
    file.close()
