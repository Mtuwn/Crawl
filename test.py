from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import base64

# # Thiết lập các tùy chọn của Chrome
# chrome_options = Options()
# chrome_options.add_argument("--disable-gpu")  # Cần thiết khi chạy trên Windows
# chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# # Khởi tạo trình duyệt Chrome với các tùy chọn đã thiết lập
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

# Mở trang web
driver.get('https://www.lazada.vn/loa-khong-day-loa-bluetooth/?up_id=2604243778&clickTrackInfo=bc4cb943-bd08-4966-9f29-53c988606f9d__10100399__2604243778__20__0.1__333258__7253__c2i__0.0__Gi%E1%BA%A3m+40%25&from=hp_categories&item_id=2604243778&version=v2&q=Loa+kh%C3%B4ng+d%C3%A2y+%26+loa+Bluetooth&params=%7B%22catIdLv1%22%3A%2210100387%22%2C%22pvid%22%3A%22bc4cb943-bd08-4966-9f29-53c988606f9d%22%2C%22src%22%3A%22ald%22%2C%22categoryName%22%3A%22Loa%2Bkh%25C3%25B4ng%2Bd%25C3%25A2y%2B%2Bloa%2BBluetooth%22%2C%22categoryId%22%3A%2210100399%22%7D&src=hp_categories')

try:
    # Chờ tối đa 20 giây cho đến khi phần tử với class 'Ms6aG MefHh' xuất hiện
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".Ms6aG.MefHh"))
    )

    # Lấy nội dung trang sau khi JavaScript đã chạy
    html = driver.page_source

    # Phân tích cú pháp HTML bằng BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Tìm tất cả các phần tử có class 'Ms6aG MefHh'
    elements = soup.select('.Ms6aG.MefHh')

    # Duyệt qua tất cả các phần tử và tìm các phần tử con tương ứng
    for idx, product in enumerate(elements, start=1):
        name_tag = product.find('div', class_='RfADt')
        price_tag = product.find('span', class_='ooOxS')
        detail_tag = product.find('span', class_='_1cEkb')
        
        name = name_tag.a['title'] if name_tag else 'N/A'
        url = name_tag.a['href'] if name_tag else 'N/A'
        
    
        price = price_tag.text if price_tag else 'N/A'
        detail = detail_tag.text if detail_tag else 'N/A'

        print(f"Product {idx}:")
        print(f"  Name: {name}")
        print(f"  Product URL: {url}")
        print(f"  Price: {price}")
        print(f"  Detail: {detail}")
        print("-" * 40)

except Exception as e:
    print("Element not found or another error occurred:", e)
finally:
    # Đóng trình duyệt
    driver.quit()
