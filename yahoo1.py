# ================== INSTALL ==================
# terminal:
# pip install psycopg2-binary beautifulsoup4 pandas

from bs4 import BeautifulSoup
from pathlib import Path
import json
import psycopg2


# ================== POSTGRES CONNECT ==================
conn = psycopg2.connect(
    host="localhost",
    port=5433,
    database="kinita",
    user="postgres",
    password="1234"
)

cur = conn.cursor()


# ================== CREATE TABLE ==================
cur.execute("""
CREATE TABLE IF NOT EXISTS skroutz_products (
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE,
    price NUMERIC,
    link TEXT
);
""")

conn.commit()


# ================== READ HTML ==================
path = Path(
    r"C:\Users\anagn\Downloads\Κινητά Τηλέφωνα Xiaomi _ Skroutz.gr.html"
)

html = path.read_text(encoding="utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")


# ================== FIND JSON-LD ==================
scripts = soup.find_all(
    "script",
    type="application/ld+json"
)


# ================== INSERT QUERY ==================
insert_query = """
INSERT INTO skroutz_products (title, price, link)
VALUES (%s, %s, %s)
ON CONFLICT (title)
DO UPDATE SET
    price = EXCLUDED.price,
    link = EXCLUDED.link;
"""


# ================== LOOP + INSERT ==================
for script in scripts:

    try:
        obj = json.loads(script.string)
    except:
        continue

    if obj.get("@type") == "ItemList":

        # ================== INSERT ==================
        for item in obj.get("itemListElement", []):

            product = item.get("item", {})

            title = product.get("name", "")
            link = product.get("url", "")
            price = product.get("offers", {}).get("price", None)

            print(title, price)

            if not title:
                continue

            try:

                cur.execute(
                    insert_query,
                    (title, price, link)
                )

                print("INSERTED")

            except Exception as e:

                print("SQL ERROR:", e)

        # ================== COMMIT ==================
        conn.commit()

        print("COMMIT OK")