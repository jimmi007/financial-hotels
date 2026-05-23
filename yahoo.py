from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
import csv

driver = webdriver.Chrome()
driver.maximize_window()

driver.get(r"file:///C:/Users/anagn/Downloads/Today's Deals.htm")

time.sleep(2)

products = driver.find_elements(By.XPATH, '//a[@data-testid="product-card-link"]')

# CSV
file = open("amazon_deals.csv", "w", newline="", encoding="utf-8-sig")
writer = csv.writer(file)

writer.writerow(["Title", "Price", "Discount", "Link"])

count = 0

for product in products:

    text = product.text.strip()

    match = re.search(r'(\d+)%\s*off', text, re.I)

    if not match:
        continue

    discount = int(match.group(1))

    if discount <= 30:
        continue

    # title
    try:
        title = product.find_element(
            By.XPATH,
            './/p[starts-with(@id,"title-")]'
        ).text.strip()
    except:
        title = "Δεν βρέθηκε"

    # price
    try:
        price = product.find_element(
            By.XPATH,
            './/*[@data-testid="price-section"]//span[contains(@class,"a-offscreen")]'
        ).text.strip()
    except:
        price = "Δεν βρέθηκε"

    # link
    link = product.get_attribute("href")

    # save csv
    writer.writerow([title, price, f"{discount}%", link])

    count += 1

    print(count, title)

    if count == 30:
        break

file.close()
driver.quit()

print("Το CSV αποθηκεύτηκε")