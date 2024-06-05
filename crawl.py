import requests
from bs4 import BeautifulSoup
import getProduct
import csv

from colorama import Fore


def fetch_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_product_info(content):
    soup = BeautifulSoup(content, 'html.parser')
    
    products = []
    for product in soup.find_all('div', class_='Bm30N'):
        name_tag = product.find('a', class_='RfADt')
        image_tag = product.find('img', class_='_95X4G')
        price_tag = product.find('span', class_='ooOxS')
        detail_tag = product.find('span', class_='lzd-article')

        if name_tag and image_tag and price_tag and detail_tag:
            name = name_tag.get('title')
            image = image_tag.get('src')
            link = name_tag.get('href')
            price = price_tag.get_text()
            detail = detail_tag.get_text()

            products.append({
                'name': name,
                'image': image,
                'link': link,
                'price': price,
                'detail': detail
            })

    return products

def generate_pagination_urls(base_url, total_pages):
    return [f"{base_url}&page={page}" for page in range(1, total_pages + 1)]

def get_category_urls(content):
    soup = BeautifulSoup(content, 'html.parser')
    category_urls = []
    
    for div in soup.find_all('div', class_='rax-view-v2 card-categories-ul'):
        a_tags = div.find_all('a')
        for a in a_tags:
            url = a.get('href')
            if url:
                if not url.startswith('http'):
                    url = 'https:' + url
                category_urls.append(url)

    return category_urls

def main():
    intro =r'''     

                                                            
                                                    ,--,    
                                                  ,--.'|    
             __  ,-.                        .---. |  | :    
           ,' ,'/ /|                       /. ./| :  : '    
   ,---.   '  | |' |    ,--.--.         .-'-. ' | |  ' |    
  /     \  |  |   ,'   /       \       /___/ \: | '  | |    
 /    / '  '  :  /    .--.  .-. |   .-'.. '   ' . |  | :    
.    ' /   |  | '      \__\/: . .  /___/ \:     ' '  : |__  
'   ; :__  ;  : |      ," .--.; |  .   \  ' .\    |  | '.'| 
'   | '.'| |  , ;     /  /  ,.  |   \   \   ' \ | ;  :    ; 
|   :    :  ---'     ;  :   .'   \   \   \  |--"  |  ,   /  
 \   \  /            |  ,     .-./    \   \ |      ---`-'   
  `----'              `--`---'         '---"                
                                                            

'''

    print(f"{Fore.GREEN}{intro}{Fore.RESET}")
    
    homepage_url = "https://www.lazada.vn"

    homepage_content = fetch_website_content(homepage_url)

    if homepage_content:
        category_urls = get_category_urls(homepage_content)
        print(f"Found {len(category_urls)} categories.")
    else:
        category_urls = []

    driver = getProduct.option()
    for base_url in category_urls:
        pagination = None
        while pagination is None:
            pagination = getProduct.page_number(driver, base_url)
        pagination_urls = generate_pagination_urls(base_url, pagination)
        
        Try = 0
        for url in pagination_urls:
            products = getProduct.info(driver, url)
            while products is None:
                if(Try == 2):
                    print("Trying!!! Please wait")
                products = getProduct.info(driver, url)
                Try += 1

            with open('products_info.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for product in products:
                    writer.writerow([product['Name'], product['Product URL'], product['Price'], product['Detail']])
            Try = 0
            print(f"Fetched products from {url}")

if __name__ == "__main__": 
    main()