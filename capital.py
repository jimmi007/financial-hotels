#  python free.py
# python free.py
# set CAPITAL_EMAIL=το_email_σου


# python free.py

# python free.py

import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://capital.com/trading/platform/portfolio")

input("Κάνε login χειροκίνητα και πάτα ENTER...")

time.sleep(5)

rows = driver.find_elements(
    By.XPATH,
    '//div[@data-testid="portfolio-instrument-container"]'
)

print("ROWS:", len(rows))

data = []

for i, row in enumerate(rows, 1):
    sinolo = row.find_element(By.XPATH, './/*[@data-testid="product-cell"]').get_attribute("innerText")
    timi = row.find_element(By.XPATH, './/*[@data-testid="instrument-margin"]').get_attribute("innerText")
    kerdos = row.find_element(By.XPATH, './/*[@data-testid="instrument-profit-loss"]').get_attribute("innerText")

    pinakas=sinolo.splitlines()
    print(pinakas)
    name = pinakas[0] if len(pinakas) > 0 else ""


    name = name.replace("CFD", "").strip()
    timi = timi.replace("\xa0", "").replace(" ", "").strip()
    kerdos = kerdos.replace("\xa0", "").replace(" ", "").strip()

    print(i, name, timi, kerdos)
    data.append([name, timi, kerdos])

with open("capital_portfolio1.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "timi", "kerdos"])
    writer.writerows(data)

print("OK CSV:", len(data))

driver.quit()