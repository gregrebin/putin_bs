import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def main(filename):
    file = open(filename, "r")
    links = file.readlines()
    file.close()
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    i = 1
    total = len(links)
    for link in links[:]:
        print(link)
        print(str(i) + "/" + str(total))
        driver.get(link)
        try:
            text = driver.find_element(By.CLASS_NAME, "read__content").text
            date = driver.find_element(By.CLASS_NAME, "read__published").get_attribute("datetime")
            with open("content/" + date + ".txt", "w") as file:
                file.write(text)
            links.remove(link)
        except Exception:
            with open(filename, "w") as file:
                for remaining in links:
                    file.write(remaining)
            return
        i += 1
        time.sleep(1)


if __name__ == '__main__':
    main("links1.txt")
