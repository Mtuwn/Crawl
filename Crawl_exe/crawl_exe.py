from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

class Crawler:
    def __init__(self):
        self.driver = webdriver.Edge()

    def load_page(self, url):
        self.List_Files = []
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.TlKaj2"))
            )

            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.select('a.TlKaj2')

            for element in elements:
                link = element.get('href', 'N/A')
                self.title = element.get('title', 'N/A')

                link = self.get_link_files(link)

                if link == -1 or "landingDownload" in link:
                    continue
                
                while "internalDownload" not in link:
                    link = self.get_link_files(link)

                file_exe = {
                    'File': self.title,
                    'link': link
                }
                self.List_Files.append(file_exe)
            return self.List_Files

        except Exception as e:
            print("Error or element not found:", e)
            return None

    def get_link_files(self, url):
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.m_rF7r.fb4o0L.HwFT3y.eQamX9"))
            )
            
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.select('a.m_rF7r.fb4o0L.HwFT3y.eQamX9')
            
            for element in elements:
                if 'js-download-btn' in element.get('class', []):
                    return -1

                link = element.get('href', 'N/A')

                if "externalDownload" in link:
                    file_exe = {
                        'File': self.title,
                        'link': link
                    }
                    self.List_Files.append(file_exe)
                    
                    return -1
                return link
        except Exception as e:
            print("Error or element not found :", e)
            return None
        
    def close(self):
        self.driver.quit()

def main():
    crawler = Crawler()
    index = 24
    
    while index <= 417:
        url = f"https://download.cnet.com/windows/{index}/"
        print(f"Processing URL: {url}")
        
        list_Files = crawler.load_page(url)
        Try = 0
        while list_Files is None:
            if(Try == 2):
                break
            list_Files = crawler.load_page(url)
            Try += 1
        print(list_Files)
        if list_Files:
            with open('File_exe.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for file in list_Files:
                    writer.writerow([file['File'], file['link']])
        index += 1
        
        
    crawler.close()

if __name__ == "__main__":
    main()
