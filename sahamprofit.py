import urllib.request
from bs4 import BeautifulSoup

def get_saham_list():
    fname = "sahamprofit.txt"
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    return [x.strip() for x in content]


list_of_links = []

def craw_and_store(next_url):

    update_stock_list_db(next_url)
    data = urllib.request.urlopen(next_url)
    soup = BeautifulSoup(data, 'html.parser')
    for i in soup.select("a[rel='prev']"):
        next_url = i._attr_value_as_string("href")
        print(next_url)
        list_of_links.append(next_url)
        craw_and_store(next_url)

def update_stock_list_db(target_url):
    # target_url = 'https://sahamprofit.co.id/2018/08/rekomendasi-saham-ihsg-8-agustus-2018/'

    data = urllib.request.urlopen(target_url)

    symbols = set(get_saham_list())

    for line in data:
        for stock in str(line).split(' '):
            if stock.isupper() and stock.strip(',|"|.').isalpha() and len(stock) == 4:
                symbols.add(stock.strip(','))

    with open("sahamprofit.txt", "w") as myfile:
        for stock in sorted(symbols):
            myfile.write(stock + "\n")


craw_and_store("https://sahamprofit.co.id/2018/08/analisa-saham-aali-target-price-14700/")
