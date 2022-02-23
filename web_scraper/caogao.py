def check_price(URL):
    

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.3 Safari/605.1.15", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id='estore_product_title').get_text()
    price = soup2.find(id='PDP_productPrice').get_text()

    title = title.strip()
    price = price.strip()[1:]

    header = ['Title', 'Price']
    data = [title, price]

    with open('ProductDataset.csv', 'w', newline='', encoding = 'UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(data)
