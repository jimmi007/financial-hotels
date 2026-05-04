from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://understat.com/league/EPL/2024")

wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

rows = driver.find_elements(By.XPATH, "//table[contains(@class,'jTable')]//tbody/tr")

print("ROWS:", len(rows))

for row in rows:
    team = row.find_element(By.XPATH, "./td[1]").text
    xpts = row.find_element(By.XPATH, "./td[last()]").text
    print({"team": team, "xPTS": xpts})

driver.quit()