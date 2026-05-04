#  python vathmologia.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import csv
from url import url3

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

driver.get(url3)
try:
    accept = wait.until(EC.element_to_be_clickable((By.XPATH, "//button")))
    accept.click()
except:
    pass

# περίμενε να εμφανιστούν αρχικά results
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="property-card"]')))

# ---------------------------
# SCROLL μέχρι να σταματήσει
# ---------------------------
last_count = 0

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    rows = driver.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
    new_count = len(rows)

    print("Loaded:", new_count)

    if new_count == last_count:
        break

    last_count = new_count

# ---------------------------
# PARSING
# ---------------------------
data = []
xaraktirismos_words = ["Καλό", "Θαυμάσιο", "Εξαιρετικό"]

rows = driver.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
print("TOTAL:", len(rows))

for i, row in enumerate(rows[:50], 1):
    try:
        row_text = row.get_attribute("innerText").strip()
        pinakas = row_text.splitlines()

        onoma = pinakas[0] if len(pinakas) > 0 else ""

        sxolia = next(
            (line for line in pinakas
             if any(word.casefold() in line.casefold() for word in xaraktirismos_words)),
            "τίποτα"
        )

        vathmos = next(
            (line for line in pinakas if re.fullmatch(r'\s*\d+,\d+\s*', line)),
            "τίποτα"
        )

        timi = next(
            (line for line in pinakas if "€" in line),
            "τίποτα"
        )

        proino = "με πρωινό" if "πρωιν" in row_text.lower() else "χωρίς ένδειξη"

        data.append([onoma, timi, vathmos, sxolia, proino])

        print(f"{i}. {onoma} | {timi} | {vathmos} | {sxolia} | {proino}")

    except Exception as e:
        print(f"error {i}: {e}")

# ---------------------------
# SAVE CSV
# ---------------------------
with open("summary.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["onoma", "timi", "vathmos", "sxolia", "proino"])
    writer.writerows(data)

driver.quit()