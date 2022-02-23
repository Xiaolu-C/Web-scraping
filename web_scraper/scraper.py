from multiprocessing import connection
from bs4 import BeautifulSoup
import requests
import datetime
import datetime
import sqlite3

def check_price(URL, user_id):
    

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.3 Safari/605.1.15", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id='estore_product_title').get_text()
    price = soup2.find(id='PDP_productPrice').get_text()

    title = title.strip()
    price = price.strip()[1:]
    today = datetime.date.today()


    # print(user_id, title, price, today)

    # 连接database

    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    with connection:
        cursor.execute("Insert into products (User_id, Date, Title, Price) values (?,?,?,?)", (user_id, today, title, price))
   


# check_price(URL=input("Link: "), user_id = input("id= "))

"""connection = sqlite3.connect('products.db')
cursor = connection.cursor()

with connection:
    cursor.execute("Insert into products (User_id, Date, Title, Price) values (?,?,?,?)", (1, 2, 3, 4))

    # 把网页数据加入table
#cursor.execute("INSERT INTO products VALUES('1','2','3','4')")"""