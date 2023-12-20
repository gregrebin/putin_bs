import time
from selenium import webdriver
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    file = open("links_short.txt", "r")
    links = file.readlines()
    file.close()
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    i = 1
    total = len(links)
    for link in links:
        print(link)
        print(str(i) + "/" + str(total))
        driver.get(link)
        try:
            text = driver.find_element(By.CLASS_NAME, "read__content").text
            date = driver.find_element(By.CLASS_NAME, "read__published").get_attribute("datetime")
            with open("content/" + date + ".txt", "w") as file:
                file.write(text)
        except Exception:
            with open("missing.txt", "a") as file:
                file.write(link)
        i += 1
        time.sleep(3)

