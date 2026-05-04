from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

base_url = "https://www.audible.com/charts/best?ref=a_hp_ndi2_i0_rowitem"

book_title = []
book_author = []
book_length = []

for page in range(1, 6):
    url = f"{base_url}&page={page}"
    print(f"\nOpening page {page}: {url}")
    driver.get(url)

    try:
        accept = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class,"truste-button1")]'))
        )
        driver.execute_script("arguments[0].click();", accept)
        print("Cookies accepted")
    except:
        pass

    products = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "li.bc-list-item.productListItem")
        )
    )

    print("Products found:", len(products))

    for i, product in enumerate(products, start=1):
        try:
            title = product.find_element(By.CSS_SELECTOR, "h3.bc-heading").text.strip()
        except:
            title = ""

        try:
            author = product.find_element(By.XPATH, './/li[contains(@class,"authorLabel")]').text.strip()
        except:
            author = ""

        try:
            length = product.find_element(By.XPATH, './/li[contains(@class,"runtimeLabel")]').text.strip()
        except:
            length = ""

        print(f"{page}.{i}: {title} | {author} | {length}")

        book_title.append(title)
        book_author.append(author)
        book_length.append(length)

driver.quit()

df_books = pd.DataFrame({
    "title": book_title,
    "author": book_author,
    "length": book_length
})

df_books.to_csv("books.csv", index=False, encoding="utf-8-sig")
print("\nSaved to books.csv")
print(df_books.head())