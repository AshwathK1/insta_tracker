import requests
from bs4 import BeautifulSoup

url = "https://www.instagram.com/dq_2024/followers/"
res = requests.get(url)
print(res.text)