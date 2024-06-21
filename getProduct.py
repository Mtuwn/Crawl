from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Khởi tạo tùy chọn Chrome để chạy ở chế độ headless và tắt hiển thị trình duyệt
def option():
    driver = webdriver.Edge()
    return driver
    
def page_number(driver, url):
    driver.get(url)
    try:
        # Sử dụng Explicit Wait để chờ cho phần tử xuất hiện
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-pagination.css-1bkhbmc.app"))
        )
        # Trích xuất danh sách các số từ nội dung của phần tử    
    except Exception as e:
        print("Error catcha")
        return None
    numbers = [int(num) for num in element.text.split() if num.isdigit()]
        # Lấy giá trị lớn nhất
    max_number = max(numbers)
    print(url)
    print("Total page:", max_number)
    return max_number

def info(driver, url):
    ListProduct = []
    driver.get(url)
    try:
        # Sử dụng Explicit Wait để chờ cho phần tử xuất hiện
        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".Ms6aG.MefHh"))
            )
        except Exception as e:
            return None
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.select('.Ms6aG.MefHh')
        for idx, product in enumerate(elements, start=1):
            name_tag = product.find('div', class_='RfADt')
            price_tag = product.find('span', class_='ooOxS')
            detail_tag = product.find('span', class_='_1cEkb')

            name = name_tag.a['title'] if name_tag else 'N/A'
            product_url = name_tag.a['href'] if name_tag else 'N/A'
            price = price_tag.text if price_tag else 'N/A'
            detail = detail_tag.text if detail_tag else 'N/A'

            product_data = {
                "Name": name,
                "Product URL": product_url,
                "Price": price,
                "Detail": detail
            }
            ListProduct.append(product_data)
            print(ListProduct)
        return ListProduct
    except Exception as e:
        print("Element not found or another error occurred:", e)
        return None

def close(driver):
    driver.quit()
