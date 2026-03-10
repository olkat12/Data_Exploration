import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

rows = []
size = 25
max_size = 18525
for offset in range(size, max_size + 1, size):
    print(f"{offset} / {max_size}")
    url = f"https://www.worldwideboxoffice.com/index.cgi?top={offset}&start=1900&finish=2026&order=worldwide"

    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.find("pre").get_text()
    pattern = re.compile(
        r"""
        \d+
        \s+\$?\s*([\d\.,]+|n/a)
        \s+\$?\s*([\d\.,]+|n/a)
        \s+\$?\s*([\d\.,]+|n/a)
        \s+(.+)
        """,
        re.VERBOSE,
    )

    for match in pattern.finditer(text):
        domestic, overseas, world, title = match.groups()
        rows.append({
            "title": title.strip(),
            "domestic_million_usd": domestic,
            "overseas_million_usd": overseas,
            "world_million_usd": world
        })

df = pd.DataFrame(rows)
df = df[df["title"] != ""]
df["year"] = df["title"].str.extract(r'\((\d+)\)')
df["title"] = df["title"].str.replace(r'\(\d+\)', '', regex=True)
df["title"] = df["title"].str.strip()
df.to_csv("../data/worldwide-box-office/boxoffice.csv", index=False)
