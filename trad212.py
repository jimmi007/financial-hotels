#  python metoxes.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5433,
    database="metoxes_db",
    user="postgres",
    password="1234"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    timi TEXT,
    deviation TEXT
)
""")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

driver.get("file:///C:/Users/anagn/Downloads/Trading%20212.htm")

rows = wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, '//div[@data-testid="eq-portfolio-tab-investment-item"]')
))

data = []


rows = driver.find_elements(By.XPATH, '//div[@data-testid="eq-portfolio-tab-investment-item"]')


def process(timi):
    match = re.search(r'[\d\.,]+\s*€', timi)

    timi = match.group() if match else ""

    return timi.replace("\xa0", "")

for i, row in enumerate(rows, 1):
    row_text = row.get_attribute("innerText").strip()
    pinakas = row_text.splitlines()
    print(pinakas)
    name = pinakas[0] if len(pinakas) > 1 else ""
    timi = pinakas[1] if len(pinakas) > 2 else ""
    timi = process(timi)

    deviation = pinakas[-1] if len(pinakas) >= 4 else ""
    match = re.search(r'\((.*?)\)', deviation)
    deviation = match.group(1) if match else ""

    print(i, name, timi, deviation)
    data.append([name, timi, deviation])





with open("metoxes4.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["name" ,"timi","deviation"])
    writer.writerows(data)

for item in data:
    cur.execute("""
        INSERT INTO products (name, timi, deviation)
        VALUES (%s, %s, %s)
        ON CONFLICT (name) DO NOTHING
    """, item)

conn.commit()

# cur.execute("DELETE FROM products WHERE title = 'Laptop Lenovo'")
conn.commit()

print("OK MPHKE")

cur.close()
conn.close()


driver.quit()