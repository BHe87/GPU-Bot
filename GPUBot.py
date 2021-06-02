import requests
import webbrowser
from bs4 import BeautifulSoup
import time

#a bot to check BestBuy if any GPUs are in stock

#path to chrome on local machine (change to your local path)
chromePath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

in_stock = {}
out_of_stock = {}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}

#links to target GPUs at BestBuy
urls = {
    'RTX 3080': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080', 
    'RTX 3070': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070', 
    'RTX 3060Ti': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti', 
    'RTX 3090': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090', 
    'RTX 3060': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060', 
    'RX 6800 XT': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206800%20XT', 
    'RX 6800': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206800', 
    'RX 6900 XT': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206900%20XT',
    'RX 6700 XT': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206700%20XT'
}


def get_all_items(soup):
    items = soup.find_all('li', class_='sku-item')

    for item in items:
        try:
            sku_header = item.find_next(class_='sku-header')
            sku_link = 'https://www.bestbuy.com' + sku_header.find_next('a').attrs['href']
            sku_title = sku_header.find_next('a').contents[0]
            sku_button = sku_header.find_next(class_='fulfillment-add-to-cart-button')
            this_button = sku_button.find_next('button')
            if this_button.contents[0] == 'Sold Out':
                out_of_stock[sku_title] = sku_link
            elif this_button.contents[1] == 'Add to Cart':
                in_stock[sku_title] = sku_link
                print('***** {} is IN STOCK\nLink: {} *****\n'.format(sku_title, sku_link))
            else:
                continue
        except:
            continue


def main():
    #continously checking the website every minute and automatically opening the webpage when GPU is in stock
    while True:
        for url in urls.items():
            print('Checking {} inventory...'.format(url[0]))
            response = requests.get(url[1], headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            get_all_items(soup)

            #success!
            if len(in_stock.items()) != 0:
                print('{} in stock now!!\n Link: {}'.format(url[0], url[1]))
                webbrowser.get(chromePath).open(url[1])

        time.sleep(60)


if __name__ == "__main__":
    main()
